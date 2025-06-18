from asyncio import gather, run
from contextlib import suppress
from queue import Empty, Queue
from threading import Thread
from typing import Any, Self, override

from websockets import ClientConnection, connect


class WebSocketClient(Thread):
    @override
    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.queue_send_messages = Queue()
        self.queue_recieve_messages = Queue()

    def get_queues(self: Self) -> tuple[Queue, Queue]:
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
                await websocket.send(self.queue_send_messages.get_nowait())

    async def recieve_messages(self: Self, websocket: ClientConnection) -> None:
        while True:
            self.queue_recieve_messages.put(await websocket.recv())
