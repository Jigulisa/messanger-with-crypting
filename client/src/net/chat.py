import asyncio
import threading
from asyncio import gather, run, sleep
from base64 import b85decode, b85encode
from contextlib import suppress
from http import HTTPStatus
from queue import Empty, Queue
from threading import Thread
from typing import Any, Self, override

from pydantic import ValidationError
from requests import RequestException, get, post
from websockets import ClientConnection, ConnectionClosed, connect

from models.is_spam import predict_spam
from net.dto import AccessChatDTO, MessageDTO
from net.utils import get_auth_headers
from secure.aead import decrypt
from secure.kdf import get_n_bytes_password
from settings import Settings


class WebSocketClient(Thread):
    @override
    def __init__(self: Self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.queue_send_messages: Queue[MessageDTO] = Queue()
        self.queue_receive_messages: Queue[MessageDTO] = Queue()
        self.running = threading.Event()
        self.stop_event = asyncio.Event()

    def get_queues(
        self: Self,
    ) -> tuple[Queue[MessageDTO], Queue[MessageDTO]]:
        return self.queue_send_messages, self.queue_receive_messages

    @override
    def run(self: Self) -> None:
        run(self.main())

    async def main(self: Self) -> None:
        while not self.running.is_set():
            with suppress(OSError):
                async with connect(
                    Settings.get_server_messages_url(),
                    additional_headers=get_auth_headers(),
                ) as websocket:
                    await gather(
                        self.send_messages(websocket),
                        self.receive_messages(websocket),
                        self.close_connection(websocket),
                    )

    async def close_connection(self: Self, websocket: ClientConnection) -> None:
        await self.stop_event.wait()
        await websocket.close()

    async def send_messages(self: Self, websocket: ClientConnection) -> None:
        while not self.running.is_set():
            try:
                message = self.queue_send_messages.get_nowait()
            except Empty:
                await sleep(0.01)
                continue

            message.signature = Settings.get_sig_key().sign(
                message.model_dump_json(exclude={"signature"}).encode(),
            )
            message_json = message.model_dump_json()
            try:
                await websocket.send(message_json)
            except ConnectionClosed:
                self.queue_send_messages.put(message)

    async def receive_messages(self: Self, websocket: ClientConnection) -> None:
        while not self.running.is_set():
            try:
                message = await websocket.recv()
            except ConnectionClosed:
                await sleep(0.01)
                continue

            try:
                verified_message = MessageDTO.model_validate_json(message)
            except ValidationError:
                continue

            is_valid = Settings.get_sig_key().verify(
                verified_message.model_dump_json(
                    exclude={"signature"},
                ).encode(),
                b85decode(verified_message.signature),
                b85decode(verified_message.author),
            )
            if is_valid:
                is_spam = predict_spam(verified_message.text)
                verified_message.is_spam = is_spam
                self.queue_receive_messages.put(verified_message)

    def stop(self: Self) -> None:
        self.running.set()
        self.stop_event.set()


def create_chat(
    secret: str,
    secret_salt: str,
    encrypted_key: str,
    key_salt: str,
    name: str,
    description: str | None = None,
) -> str | None:
    data = {
        "chat_name": name,
        "description": description,
        "secret": secret,
        "secret_salt": secret_salt,
        "key": encrypted_key,
        "key_salt": key_salt,
    }

    try:
        response = post(
            Settings.get_server_chat_url("/create"),
            json=data,
            timeout=10,
            headers=get_auth_headers(),
        )
    except RequestException:
        return None

    if response.status_code != HTTPStatus.CREATED:
        return None

    return response.json()


def get_user_kem_public_key(username: str) -> str | None:
    data = {
        "username": username,
    }
    try:
        response = get(
            Settings.get_server_users_url("/kem"),
            params=data,
            timeout=10,
            headers=get_auth_headers(),
        )
    except RequestException:
        return None

    if response.status_code != HTTPStatus.OK:
        return None

    return response.text


def grant_access(chat_uuid: str, user: str) -> None:
    user_kem_public_key = get_user_kem_public_key(user)
    if user_kem_public_key is None:
        return

    secret, secret_salt, encrypted_key, key_salt = (
        Settings.get_kem_key().encap_chat_key(
            user_kem_public_key,
            b85encode(Settings.get_chat_key(chat_uuid)).decode(),
        )
    )
    data = {
        "chat_id": chat_uuid,
        "user": user,
        "secret": secret,
        "secret_salt": secret_salt,
        "key": encrypted_key,
        "key_salt": key_salt,
    }
    with suppress(RequestException):
        post(
            Settings.get_server_chat_url("/grant"),
            json=data,
            timeout=10,
            headers=get_auth_headers(),
        )


def get_all_chats() -> None:
    try:
        response = get(
            Settings.get_server_chat_url("/all"),
            timeout=10,
            headers=get_auth_headers(),
        )
    except RequestException:
        return

    if response.status_code != HTTPStatus.OK:
        return

    access_list = response.json()

    chats = Settings.get_chats()
    for chat in set(chats.keys()).difference(
        {access["chat_id"] for access in access_list},
    ):
        chats.pop(chat)

    for chat in access_list:
        access = AccessChatDTO.model_validate(chat)
        secret = Settings.get_kem_key().decap_secret(access.secret)
        password, _ = get_n_bytes_password(secret, 32, b85decode(access.secret_salt))
        key = decrypt(password, access.key, access.key_salt)
        uuid = str(access.chat_id)
        chats[uuid] = {
            "name": access.chat_name or uuid,
            "key": key,
        }

    Settings.set_chats(chats)


def get_all_messages(chat_uuid: str) -> list[MessageDTO] | None:
    try:
        response = get(
            Settings.get_server_chat_url(f"/{chat_uuid}"),
            timeout=10,
            headers=get_auth_headers(),
        )
    except RequestException:
        return None

    if response.status_code != HTTPStatus.OK:
        return None

    return [MessageDTO.model_validate(message) for message in response.json()]
