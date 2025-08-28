from base64 import b85decode
from typing import Literal
from uuid import UUID

from settings.storage import Storage

type Chat = dict[Literal["name", "key"], str]


class ChatsMixin:
    @staticmethod
    def set_chats(chats: dict[str, Chat]) -> dict[str, Chat]:
        return Storage[dict[str, Chat]].set_value("chats", chats)

    @staticmethod
    def add_chat(name: str, uuid: str, key: str) -> str:
        chats = Storage[dict[str, Chat]].get_value("chats", default={})
        chats[uuid] = {
            "name": name,
            "key": key,
        }
        ChatsMixin.set_chats(chats)
        return name

    @staticmethod
    def get_chats() -> dict[str, Chat]:
        return Storage[dict[str, Chat]].get_value("chats", default={})

    @staticmethod
    def get_chat(uuid: str) -> Chat:
        return ChatsMixin.get_chats()[uuid]

    @staticmethod
    def get_chat_name(uuid: str) -> str:
        return ChatsMixin.get_chat(uuid)["name"]

    @staticmethod
    def get_chat_key(uuid: UUID | str) -> bytes:
        if isinstance(uuid, UUID):
            uuid = str(uuid)
        return b85decode(ChatsMixin.get_chat(uuid)["key"])
