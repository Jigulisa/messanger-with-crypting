from base64 import b85decode
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any, Self, override

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware.authentication import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)
from litestar.stores.memory import MemoryStore
from oqs import Signature

from users.dependencies import provide_user_repository
from users.models.repositories import UserRepository

if TYPE_CHECKING:
    from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig


class AuthenticationMiddleware(AbstractAuthenticationMiddleware):
    @override
    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        self.sqlalchemy_config: SQLAlchemyAsyncConfig = kwargs.pop("sqlalchemy_config")
        super().__init__(*args, **kwargs)
        self.store = MemoryStore()

    @staticmethod
    def get_header(connection: ASGIConnection, header: str) -> str:
        value = connection.headers.get(header)
        if value is None:
            raise NotAuthorizedException
        return value

    @asynccontextmanager
    async def get_user_repository(self) -> AsyncGenerator[UserRepository]:
        async with self.sqlalchemy_config.get_session() as session, session.begin():
            yield await provide_user_repository(session)

    def check_timestamp(self: Self, connection: ASGIConnection) -> None:
        timestamp = datetime.fromisoformat(self.get_header(connection, "X-Timestamp"))

        if datetime.now(UTC) < timestamp:
            raise NotAuthorizedException

        if datetime.now(UTC) - timestamp > timedelta(minutes=1):
            raise NotAuthorizedException

    async def check_replay(self: Self, connection: ASGIConnection) -> tuple[str, str]:
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

        return public_key, nonce

    def check_signature(
        self: Self,
        connection: ASGIConnection,
        public_key: str,
        nonce: str,
    ) -> None:
        signature = self.get_header(connection, "X-Signature")
        with Signature("ML-DSA-87") as verifier:
            is_valid = verifier.verify(
                b85decode(nonce),
                b85decode(signature),
                b85decode(public_key),
            )

        if not is_valid:
            raise NotAuthorizedException

    async def authenticate_request(
        self: Self,
        connection: ASGIConnection,
    ) -> AuthenticationResult:
        self.check_timestamp(connection)
        public_key, nonce = await self.check_replay(connection)
        self.check_signature(connection, public_key, nonce)

        async with self.get_user_repository() as user_repository:
            user, _ = await user_repository.get_or_upsert(
                public_key=public_key,
                upsert=False,
            )

        return AuthenticationResult(user=user, auth=public_key)
