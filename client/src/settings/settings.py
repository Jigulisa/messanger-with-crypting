from settings.chats import ChatsMixin
from settings.keys import KeysMixin
from settings.server import ServerMixin
from settings.storage import Storage


class Settings(KeysMixin, ChatsMixin, ServerMixin):
    @staticmethod
    def get_hf_token() -> str:
        return Storage[str].get_value("hf_token")
