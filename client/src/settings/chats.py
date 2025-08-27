from typing import Literal
from uuid import UUID

from secure.aead import generate_key
from settings.storage import Storage

type Chat = dict[Literal["uuid", "key"], str]


class ChatsMixin:
    @staticmethod
    def add_chat(name: str, uuid: str) -> str:
        chats = Storage[dict[str, Chat]].get_value("chats", default={})
        chats[name] = {
            "uuid": uuid,
            "key": generate_key(),
        }
        Storage[dict[str, Chat]].set_value("chats", chats)
        return name

    @staticmethod
    def get_chats() -> dict[str, Chat]:
        return Storage[dict[str, Chat]].get_value("chats", default={})

    @staticmethod
    def get_chat(name: str) -> Chat:
        return ChatsMixin.get_chats()[name]

    @staticmethod
    def get_chat_uuid(name: str) -> UUID:
        return UUID(ChatsMixin.get_chat(name)["uuid"])

    @staticmethod
    def get_chet_key(name: str) -> str:
        return ChatsMixin.get_chat(name)["key"]
