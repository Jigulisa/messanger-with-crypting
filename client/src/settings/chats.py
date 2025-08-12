from settings.storage import Storage


class ChatsMixin:
    @staticmethod
    def add_chat(new_chat: str) -> str:
        chats = set(Storage[list].get_value("chats", default=[]))
        chats.add(new_chat)
        Storage[list].set_value("chats", list(chats))
        return new_chat

    @staticmethod
    def delete_chat(chat: str) -> str:
        chats = set(Storage[list].get_value("chats", default=[]))
        chats.remove(chat)
        Storage[list].set_value("chats", list(chats))
        return chat

    @staticmethod
    def get_chats() -> set[str]:
        return set(Storage[list].get_value("chats", default=[]))
