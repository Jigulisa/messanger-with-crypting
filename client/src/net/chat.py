from asyncio import gather, run
from base64 import b85decode
from contextlib import suppress
from queue import Empty, Queue
from threading import Thread
from typing import Any, Self, override

from pydantic import ValidationError
from websockets import ClientConnection, connect

from net.message_struct import ReceivedPrivateMessage, SentPrivateMessage
from settings.settings import Settings
from secure.signature import sign, verify


class WebSocketClient(Thread):
    @override
    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.queue_send_messages = Queue()
        self.queue_receive_messages = Queue()

    def get_queues(
        self: Self,
    ) -> tuple[Queue[SentPrivateMessage], Queue[ReceivedPrivateMessage]]:
        return self.queue_send_messages, self.queue_receive_messages

    @override
    def run(self) -> None:
        run(self.main())

    def get_auth_headers(self: Self) -> dict[str, str]:
        return {}

    async def main(self: Self) -> None:
        async with connect("ws://127.0.0.1:8000/messages") as websocket:
            await gather(
                self.send_messages(websocket),
                self.receive_messages(websocket),
            )

    async def send_messages(self: Self, websocket: ClientConnection) -> None:
        while True:
            with suppress(Empty):
                message = self.queue_send_messages.get_nowait()
                message.signature = sign(
                    message.model_dump_json(exclude={"signature"}).encode(),
                    Settings.get_private_key(),
                )
                message_json = message.model_dump_json()
                await websocket.send(message_json)

    async def receive_messages(self: Self, websocket: ClientConnection) -> None:
        while True:
            message = await websocket.recv()
            try:
                message_stuct = ReceivedPrivateMessage.model_validate_json(message)
            except ValidationError:
                continue

            is_valid = verify(
                message_stuct.model_dump_json(exclude={"signature", "spam"}).encode(),
                b85decode(message_stuct.signature),
                b85decode(message_stuct.author),
            )
            if is_valid:
                self.queue_receive_messages.put(message_stuct)
