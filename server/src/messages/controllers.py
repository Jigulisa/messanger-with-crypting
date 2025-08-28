from base64 import b85decode
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress
from typing import Self
from uuid import UUID

from litestar import Controller, Request, WebSocket, get, post, websocket_listener
from litestar.channels import ChannelsPlugin
from litestar.exceptions import (
    PermissionDeniedException,
    WebSocketDisconnect,
)
from oqs import Signature
from pydantic import ValidationError

from messages.models.dto import AccessChatDTO, CreateChat, GrantAccess, MessageDTO
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
        access_repository: AccessRepository,
    ) -> None:
        self.socket = socket
        self.access_repository = access_repository

    @staticmethod
    def validate(data: bytes | str) -> MessageDTO | None:
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

        if await self.access_repository.exists(
            chat_id=message.chat_id,
            user=self.socket.user,
        ):
            await self.socket.send_data(message.model_dump_json())


@asynccontextmanager
async def messages_connection_lifespan(
    socket: WebSocket,
    channels: ChannelsPlugin,
    access_repository: AccessRepository,
) -> AsyncGenerator[None]:
    async with (
        channels.start_subscription("messages_channel") as subscriber,
        subscriber.run_in_background(
            MessageCallback(
                socket,
                access_repository,
            ),
        ),
    ):
        with suppress(WebSocketDisconnect):
            yield


@websocket_listener("/", connection_lifespan=messages_connection_lifespan)
async def messages(
    socket: WebSocket,
    data: str,
    channels: ChannelsPlugin,
    message_repository: MessageRepository,
) -> None:
    message = MessageCallback.validate(data)
    if message is None:
        return
    if socket.auth != message.author:
        return

    await message_repository.add(
        Message(
            text=message.text,
            salt=message.salt,
            sent_time=message.sent_time,
            author=socket.user,
            chat_id=message.chat_id,
            signature=message.signature,
        ),
        auto_commit=True,
    )
    await channels.wait_published(data, "messages_channel")


class ChatsCallback:
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

    async def __call__(self: Self, data: bytes) -> None: ...


@asynccontextmanager
async def chats_connection_lifespan(
    socket: WebSocket,
    channels: ChannelsPlugin,
    user_repository: UserRepository,
    message_repository: MessageRepository,
    access_repository: AccessRepository,
) -> AsyncGenerator[None]:
    async with (
        channels.start_subscription("chats_channel") as subscriber,
        subscriber.run_in_background(
            ChatsCallback(
                socket,
                user_repository,
                message_repository,
                access_repository,
            ),
        ),
    ):
        with suppress(WebSocketDisconnect):
            yield


@websocket_listener("/chats", connection_lifespan=chats_connection_lifespan)
async def chats(data: str, channels: ChannelsPlugin) -> None:
    await channels.wait_published(data, "chats_channel")


class ChatController(Controller):
    path = "/chat"

    @post("/create")
    async def create_chat(
        self: Self,
        request: Request,
        data: CreateChat,
        chat_repository: ChatRepository,
        access_repository: AccessRepository,
    ) -> UUID:
        dict_data = data.model_dump()
        chat = await chat_repository.add(
            Chat(description=dict_data.pop("description"), owner=request.user),
            auto_commit=True,
        )
        await access_repository.add(
            Access(user=request.user, chat=chat, role=request.auth, **dict_data),
            auto_commit=True,
        )
        return chat.id

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
        access_data = data.model_dump()
        access_data["user"] = user
        await access_repository.add(Access(**access_data))

    @get("/{chat_id:uuid}")
    async def get_chat_messages(
        self: Self,
        request: Request,
        chat_id: UUID,
        access_repository: AccessRepository,
        message_repository: MessageRepository,
    ) -> list[MessageDTO]:
        if not await access_repository.exists(user=request.user, chat_id=chat_id):
            raise PermissionDeniedException
        return [
            MessageDTO(
                text=message.text,
                salt=message.salt,
                sent_time=message.sent_time,
                author=message.author.dsa_public_key,
                chat_id=chat_id,
                signature=message.signature,
            )
            for message in await message_repository.list(chat_id=chat_id)
        ]

    @get("/all")
    async def get_all_chats(
        self: Self,
        request: Request,
        access_repository: AccessRepository,
    ) -> list[AccessChatDTO]:
        return [
            AccessChatDTO(
                chat_id=access.chat_id,
                chat_name=access.chat_name,
                secret=access.secret,
                secret_salt=access.secret_salt,
                key=access.key,
                key_salt=access.key_salt,
            )
            for access in await access_repository.list(user=request.user)
        ]
