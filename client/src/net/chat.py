from asyncio import gather, run
from contextlib import suppress
from queue import Empty, Queue
from threading import Thread
from typing import Any, Self, override

from oqs import Signature
from pydantic import ValidationError
from websockets import ClientConnection, connect

from net.message_struct import ReceivedPrivateMessage, SentPrivateMessage
from settings.settings import Settings


class WebSocketClient(Thread):
    @override
    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.queue_send_messages = Queue()
        self.queue_recieve_messages = Queue()

    def get_queues(
        self: Self,
    ) -> tuple[Queue[SentPrivateMessage], Queue[ReceivedPrivateMessage]]:
        return self.queue_send_messages, self.queue_recieve_messages

    @override
    def run(self) -> None:
        run(self.main())

    async def main(self: Self) -> None:
        async with connect("ws://127.0.0.1:8000/messages") as websocket:
            await gather(
                self.send_messages(websocket),
                self.recieve_messages(websocket),
            )

    async def send_messages(self: Self, websocket: ClientConnection) -> None:
        while True:
            with suppress(Empty):
                message = self.queue_send_messages.get_nowait()
                with Signature("ML-DSA-87", Settings.get_private_key_bytes()) as signer:
                    signature = signer.sign(
                        message.model_dump_json(exclude={"signature"}).encode(),
                    )
                message.signature = signature
                message_json = message.model_dump_json()
                await websocket.send(message_json)

    async def recieve_messages(self: Self, websocket: ClientConnection) -> None:
        while True:
            message = await websocket.recv()
            with suppress(ValidationError):
                message_stuct = ReceivedPrivateMessage.model_validate_json(message)
                self.queue_recieve_messages.put(message_stuct)
