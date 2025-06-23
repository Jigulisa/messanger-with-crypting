from base64 import b85decode
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress
from datetime import UTC, datetime, timedelta
from typing import Any, Self, override

from litestar import Litestar, WebSocket, websocket_listener
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException, WebSocketDisconnect
from litestar.middleware import DefineMiddleware
from litestar.middleware.authentication import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)
from litestar.stores.memory import MemoryStore
from oqs import Signature

from message_callback import MessageCallback


class AuthenticationMiddleware(AbstractAuthenticationMiddleware):
    @override
    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.store = MemoryStore()

    @staticmethod
    def get_header(connection: ASGIConnection, header: str) -> str:
        value = connection.headers.get(header)
        if value is None:
            raise NotAuthorizedException
        return value

    async def authenticate_request(
        self: Self,
        connection: ASGIConnection,
    ) -> AuthenticationResult:
        timestamp = datetime.fromisoformat(self.get_header(connection, "X-Timestamp"))
        if datetime.now(UTC) - timestamp > timedelta(minutes=1):
            raise NotAuthorizedException

        public_key = self.get_header(connection, "X-Public-Key")
        nonce = self.get_header(connection, "X-Nonce")
        key = f"{public_key}:{nonce}"

        if await self.store.exists(key):
            raise NotAuthorizedException
        await self.store.set(
            key,
            value="",
            expires_in=timedelta(minutes=1),
        )

        signature = self.get_header(connection, "X-Signature")
        with Signature("ML-DSA-87") as verifier:
            is_valid = verifier.verify(
                b85decode(nonce),
                b85decode(signature),
                b85decode(public_key),
            )
        if not is_valid:
            raise NotAuthorizedException

        return AuthenticationResult(user=public_key, auth=public_key)


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


@websocket_listener("/messages", connection_lifespan=connection_lifespan)
async def messages(data: str, channels: ChannelsPlugin) -> None:
    await channels.wait_published(data, "messages_channel")


app = Litestar(
    route_handlers=[messages],
    plugins=[
        ChannelsPlugin(backend=MemoryChannelsBackend(), channels=["messages_channel"]),
    ],
    middleware=[DefineMiddleware(AuthenticationMiddleware)],
)
