import asyncio
import threading
from asyncio import gather, run, sleep
from base64 import b85decode
from contextlib import suppress
from http import HTTPStatus
from queue import Empty, Queue
from threading import Thread
from typing import Any, Self, override
from uuid import UUID

from pydantic import ValidationError
from requests import RequestException, post
from websockets import ClientConnection, ConnectionClosed, connect

from models.is_spam import predict_spam
from net.message_struct import PrivateMessage
from net.utils import get_auth_headers
from secure.signature import sign, verify
from settings import Settings


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

    async def main(self: Self) -> None:
        while not self.running.is_set():
            with suppress(OSError):
                async with connect(
                    Settings.get_server_messages_url(),
                    additional_headers=get_auth_headers(),
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
                is_spam = bool(predict_spam(verified_message.message))
                verified_message.is_spam = is_spam
                self.queue_receive_messages.put(verified_message)

    def stop(self: Self) -> None:
        self.running.set()
        self.stop_event.set()


def create_chat(name: str, description: str | None = None) -> UUID | None:
    data = {
        "name": name,
        "description": description,
    }

    try:
        response = post(
            Settings.get_server_chat_url("/create"),
            json=data,
            timeout=10,
            headers=get_auth_headers(),
        )
    except RequestException:
        return None

    if response.status_code != HTTPStatus.CREATED:
        return None

    return UUID(response.text)
