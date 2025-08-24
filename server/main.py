from base64 import b85decode
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Self, override
from zoneinfo import ZoneInfo

from litestar import Litestar, Response, WebSocket, get, post, websocket_listener
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException, WebSocketDisconnect
from litestar.middleware import DefineMiddleware
from litestar.middleware.authentication import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)
from litestar.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from litestar.stores.memory import MemoryStore
from message_callback import MessageCallback
from message_struct import (
    AllFileNamesModel,
    DeleteModel,
    DownloadFileModel,
    GetFilePropertiesModel,
    RenameModel,
)
from oqs import Signature

if not (Path(__file__).parent / "storage").exists():
    (Path(__file__).parent / "storage").mkdir()


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

#        __
# |   | /  \ |    |
# |\  | |  | |    |
# | \ | |  | | /\ |
# |  \| \__/ \/  \/    HTTP

# больше я никогда не буду программистом клянусь


@get("/get_file_names")
def get_file_names(user: str) -> Response:
    folder_path = Path(__file__).parent / f"storage/{user}"
    if not folder_path.exists():
        folder_path.mkdir()
        resp = AllFileNamesModel(names=[])
        return Response(content=resp, status_code=HTTP_200_OK)

    files = [file.name for file in folder_path.iterdir()]
    resp = AllFileNamesModel(names=files)
    return Response(content=resp, status_code=HTTP_200_OK)


@get("/download_file")
async def download_file(user: str, name: str) -> Response:
    path = Path(__file__).parent / f"storage/{user}/{name}"
    content = path.read_bytes()
    resp = DownloadFileModel(data=content)
    return Response(content=resp, status_code=HTTP_200_OK)


@post("/rename")
def rename(user: str, old: str, new: str) -> Response:
    old_file = Path(__file__).parent / f"storage/{user}/{old}"
    new_file = Path(__file__).parent / f"storage/{user}/{new}"
    try:
        old_file.rename(new_file)
    except Exception:
        resp = RenameModel(message="Error. Try again.")
        return Response(content=resp, status_code=HTTP_400_BAD_REQUEST)

    resp = RenameModel(message="Ok.")
    return Response(content=resp, status_code=HTTP_200_OK)


@get("/get_file_properties")
def get_file_properties(user: str, name: str) -> Response:
    path = Path(__file__).parent / f"storage/{user}/{name}"
    try:
        stats = path.stat()
        birth_datetime = datetime.fromtimestamp(
            stats.st_birthtime,
            ZoneInfo("Europe/Moscow"),
        )
        last_datetime = datetime.fromtimestamp(
            stats.st_atime,
            ZoneInfo("Europe/Moscow"),
        )
        resp = GetFilePropertiesModel(
            name=name.split(".")[0],
            load_time=birth_datetime,
            size=stats.st_size,
            last_touched=last_datetime,
        )
        return Response(content=resp, status_code=HTTP_200_OK)
    except Exception:
        return Response(content=None, status_code=HTTP_404_NOT_FOUND)


@post("/delete_file")
def delete_file(user: str, name: str) -> Response:
    path = Path(__file__).parent / f"storage/{user}/{name}"
    if not path.exists():
        resp = DeleteModel(message="Error occured.")
        return Response(content=resp, status_code=HTTP_404_NOT_FOUND)
    path.unlink()
    resp = DeleteModel(message="File deleted.")
    return Response(content=resp, status_code=HTTP_200_OK)
