from settings.storage import Storage


class ChatsMixin:
    @staticmethod
    def add_chat(name: str, uuid: str) -> str:
        chats = Storage[dict[str, str]].get_value("chats", default={})
        chats[name] = uuid
        Storage[dict[str, str]].set_value("chats", chats)
        return name

    @staticmethod
    def get_chats() -> dict[str, str]:
        return Storage[dict[str, str]].get_value("chats", default={})
