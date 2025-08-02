from enum import Enum

from gui.views.chat import Chat
from gui.views.settings import Settings
from gui.views.storage import Storage
from gui.views.search import Search

class ViewName(Enum):
    CHAT = Chat()
    SETTINGS = Settings()
    STORAGE = Storage()
    SEARCH = Search()