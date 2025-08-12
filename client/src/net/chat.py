import asyncio
import threading
from asyncio import gather, run, sleep
from base64 import b85decode, b85encode
from contextlib import suppress
from datetime import UTC, datetime
from os import urandom
from queue import Empty, Queue
from threading import Thread
from typing import Any, Self, override

from pydantic import ValidationError
from websockets import ClientConnection, ConnectionClosed, connect

from models.is_spam import predict_spam
from net.message_struct import PrivateMessage
from secure.signature import sign, verify
from settings.settings import Settings


class WebSocketClient(Thread):
    @override
    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.queue_send_messages: Queue[PrivateMessage] = Queue()
        self.queue_receive_messages: Queue[PrivateMessage] = Queue()
        self.running = threading.Event()
        self.stop_event = asyncio.Event()

    def get_queues(
        self: Self,
    ) -> tuple[Queue[PrivateMessage], Queue[PrivateMessage]]:
        return self.queue_send_messages, self.queue_receive_messages

    @override
    def run(self: Self) -> None:
        run(self.main())

    def get_auth_headers(self: Self) -> dict[str, str]:
        nonce = urandom(2048)
        return {
            "X-Timestamp": datetime.now(UTC).isoformat(),
            "X-Public-Key": Settings.get_public_key(),
            "X-Nonce": b85encode(nonce).decode(),
            "X-Signature": sign(nonce, Settings.get_private_key()),
        }

    async def main(self: Self) -> None:
        while not self.running.is_set():
            with suppress(OSError):
                async with connect(
                    "ws://127.0.0.1:8000/messages",
                    additional_headers=self.get_auth_headers(),
                ) as websocket:
                    await gather(
                        self.send_messages(websocket),
                        self.receive_messages(websocket),
                        self.close_connection(websocket),
                    )

    async def close_connection(self: Self, websocket: ClientConnection) -> None:
        await self.stop_event.wait()
        await websocket.close()

    async def send_messages(self: Self, websocket: ClientConnection) -> None:
        while not self.running.is_set():
            try:
                message = self.queue_send_messages.get_nowait()
            except Empty:
                await sleep(0.01)
                continue

            message.signature = sign(
                message.model_dump_json(exclude={"signature"}).encode(),
                Settings.get_private_key(),
            )
            message_json = message.model_dump_json()
            try:
                await websocket.send(message_json)
            except ConnectionClosed:
                self.queue_send_messages.put(message)

    async def receive_messages(self: Self, websocket: ClientConnection) -> None:
        while not self.running.is_set():
            try:
                message = await websocket.recv()
            except ConnectionClosed:
                await sleep(0.01)
                continue

            try:
                verified_message = PrivateMessage.model_validate_json(message)
            except ValidationError:
                continue

            is_valid = verify(
                verified_message.model_dump_json(
                    exclude={"signature"},
                ).encode(),
                b85decode(verified_message.signature),
                b85decode(verified_message.author),
            )
            if is_valid:
                is_spam = bool(predict_spam(verified_message))
                verified_message.is_spam = is_spam
                self.queue_receive_messages.put(verified_message)

    def stop(self: Self) -> None:
        self.running.set()
        self.stop_event.set()
