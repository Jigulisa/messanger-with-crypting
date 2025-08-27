from uuid import UUID

from settings.storage import Storage


class ChatsMixin:
    @staticmethod
    def add_chat(name: str, uuid: UUID) -> str:
        chats = set(Storage[list].get_value("chats", default=[]))
        chats.add({"name": name, "uuid": uuid})
        Storage[list].set_value("chats", list(chats))
        return name

    @staticmethod
    def delete_chat(name: str) -> str:
        chats = set(Storage[list].get_value("chats", default=[]))
        chats.remove(name)
        Storage[list].set_value("chats", list(chats))
        return name

    @staticmethod
    def get_chats() -> set[str]:
        return set(Storage[list].get_value("chats", default=[]))
