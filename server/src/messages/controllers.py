from base64 import b85decode
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress
from typing import Self

from litestar import WebSocket, websocket_listener
from litestar.channels import ChannelsPlugin
from litestar.exceptions import WebSocketDisconnect
from oqs import Signature
from pydantic import ValidationError

from messages.models.dto import PrivateMessage


class MessageCallback:
    def __init__(self: Self, socket: WebSocket) -> None:
        self.socket = socket

    @staticmethod
    def validate(data: bytes) -> PrivateMessage | None:
        try:
            message = PrivateMessage.model_validate_json(data)
        except ValidationError:
            return None
        with Signature("ML-DSA-87") as verifier:
            is_valid = verifier.verify(
                message.model_dump_json(exclude={"signature"}).encode(),
                b85decode(message.signature),
                b85decode(message.author),
            )
        return message if is_valid else None

    async def __call__(self: Self, data: bytes) -> None:
        message = self.validate(data)
        if message is None:
            return
        if self.socket.auth in {message.receive_id, message.author}:
            await self.socket.send_data(message.model_dump_json())


@asynccontextmanager
async def connection_lifespan(
    socket: WebSocket,
    channels: ChannelsPlugin,
) -> AsyncGenerator[None]:
    async with (
        channels.start_subscription("messages_channel") as subscriber,
        subscriber.run_in_background(MessageCallback(socket)),
    ):
        with suppress(WebSocketDisconnect):
            yield


@websocket_listener("/", connection_lifespan=connection_lifespan)
async def messages(data: str, channels: ChannelsPlugin) -> None:
    await channels.wait_published(data, "messages_channel")
