from settings.chats import ChatsMixin
from settings.keys import KeysMixin
from settings.server import ServerMixin


class Settings(KeysMixin, ChatsMixin, ServerMixin): ...
