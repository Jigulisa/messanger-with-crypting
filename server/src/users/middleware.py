from base64 import b85decode
from datetime import UTC, datetime, timedelta
from typing import Any, Self, override

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import DefineMiddleware
from litestar.middleware.authentication import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)
from litestar.stores.memory import MemoryStore
from oqs import Signature

from users.dependencies import dependencies


class AuthenticationMiddleware(AbstractAuthenticationMiddleware):
    @override
    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        self.user_repository = kwargs.pop("user_repository")
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

        user, _ = await self.user_repository.get_or_upsert(public_key=public_key)
        return AuthenticationResult(user=user, auth=public_key)


middleware = [
    DefineMiddleware(
        AuthenticationMiddleware,
        user_repository=dependencies["user_repository"],
        exclude=["/schema/swagger"],
    ),
]
