from base64 import b85decode
from typing import Literal
from uuid import UUID

from settings.storage import Storage

type Chat = dict[Literal["uuid", "key"], str]


class ChatsMixin:
    @staticmethod
    def add_chat(name: str, uuid: str, key: str) -> str:
        chats = Storage[dict[str, Chat]].get_value("chats", default={})
        chats[name] = {
            "uuid": uuid,
            "key": key,
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
    def get_chat_key(name: str) -> bytes:
        return b85decode(ChatsMixin.get_chat(name)["key"])

    @staticmethod
    def get_chat_key_by_uuid(uuid: UUID) -> bytes:
        for chat in ChatsMixin.get_chats().values():
            if chat["uuid"] == str(uuid):
                return b85decode(chat["key"])
        raise KeyError
