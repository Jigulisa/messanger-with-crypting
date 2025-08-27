from base64 import b85decode
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress
from typing import Self
from uuid import UUID

from litestar import Controller, Request, WebSocket, get, post, websocket_listener
from litestar.channels import ChannelsPlugin
from litestar.exceptions import (
    ClientException,
    PermissionDeniedException,
    WebSocketDisconnect,
)
from oqs import Signature
from pydantic import ValidationError

from messages.models.dto import CreateChat, GrantAccess, MessageDTO
from messages.models.orm import Access, Chat, Message
from messages.models.repositories import (
    AccessRepository,
    ChatRepository,
    MessageRepository,
)
from users.models.repositories import UserRepository


class MessageCallback:
    def __init__(
        self: Self,
        socket: WebSocket,
        user_repository: UserRepository,
        message_repository: MessageRepository,
        access_repository: AccessRepository,
    ) -> None:
        self.socket = socket
        self.user_repository = user_repository
        self.message_repository = message_repository
        self.access_repository = access_repository

    @staticmethod
    def validate(data: bytes) -> MessageDTO | None:
        try:
            message = MessageDTO.model_validate_json(data)
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

        author = await self.user_repository.get_one(public_key=message.author)
        await self.message_repository.add(
            Message(
                sent_time=message.sent_time,
                text=message.text,
                author=author,
                chat_id=message.chat_id,
            ),
            auto_commit=True,
        )

        chat_users = {access.user.public_key for access in await self.access_repository.list(chat_id=message.chat_id)}

        if self.socket.auth in chat_users:
            await self.socket.send_data(message.model_dump_json())


@asynccontextmanager
async def connection_lifespan(
    socket: WebSocket,
    channels: ChannelsPlugin,
    user_repository: UserRepository,
    message_repository: MessageRepository,
    access_repository: AccessRepository,
) -> AsyncGenerator[None]:
    async with (
        channels.start_subscription("messages_channel") as subscriber,
        subscriber.run_in_background(
            MessageCallback(socket, user_repository, message_repository, access_repository),
        ),
    ):
        with suppress(WebSocketDisconnect):
            yield


@websocket_listener("/", connection_lifespan=connection_lifespan)
async def messages(data: str, channels: ChannelsPlugin) -> None:
    await channels.wait_published(data, "messages_channel")


class ChatController(Controller):
    path = "/chat"

    @post("/create")
    async def create_chat(
        self: Self,
        request: Request,
        data: CreateChat,
        chat_repository: ChatRepository,
    ) -> None:
        if await chat_repository.exists(owner=request.user, name=data.name):
            raise ClientException(detail="Chat with this name already exists")
        chat = Chat(**data.model_dump(), owner=request.user)
        await chat_repository.add(chat, auto_commit=True)

    @post("/grant")
    async def grant_access(
        self: Self,
        request: Request,
        data: GrantAccess,
        chat_repository: ChatRepository,
        user_repository: UserRepository,
        access_repository: AccessRepository,
    ) -> None:
        chat = await chat_repository.get(data.chat_id)
        if request.user != chat.owner:
            raise PermissionDeniedException
        user = await user_repository.get_one(public_key=data.user)
        await access_repository.add(Access(user=user, chat=chat, role=data.user))

    @get("/{chat_id:int}")
    async def get_chat_messages(
        self: Self,
        request: Request,
        chat_id: UUID,
        access_repository: AccessRepository,
        message_repository: MessageRepository,
    ) -> list[MessageDTO]:
        if await access_repository.exists(user=request.user, chat_id=chat_id):
            raise ClientException(detail="Chat with this name already exists")
        return [
            MessageDTO(
                text=message.text,
                sent_time=message.sent_time,
                author=message.author.public_key,
                chat_id=chat_id,
                signature=message.signature,
            )
            for message in await message_repository.list(chat_id=chat_id)
        ]
