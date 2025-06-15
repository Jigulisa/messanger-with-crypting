from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Self

from litestar import Litestar, WebSocket
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend
from litestar.handlers import websocket_listener


class ChannelCallback:
    def __init__(self: Self, socket: WebSocket) -> None:
        self.socket = socket

    async def __call__(self: Self, data: bytes) -> None:
        await self.socket.send_data(data)


@asynccontextmanager
async def connection_lifespan(
    socket: WebSocket,
    channels: ChannelsPlugin,
) -> AsyncGenerator[None]:
    async with (
        channels.start_subscription("channel") as subscriber,
        subscriber.run_in_background(ChannelCallback(socket)),
    ):
        yield


@websocket_listener("/", connection_lifespan=connection_lifespan)
async def handler(data: str, channels: ChannelsPlugin) -> None:
    await channels.wait_published(data, "channel")


app = Litestar(
    route_handlers=[handler],
    plugins=[ChannelsPlugin(backend=MemoryChannelsBackend(), channels=["channel"])],
)
