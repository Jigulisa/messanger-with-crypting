from enum import Enum

from gui.views.chat import Chat
from gui.views.search import Search
from gui.views.settings import Settings
from gui.views.storage import Storage
from gui.views.help_page import HelpPage


class ViewName(Enum):
    CHAT = Chat()
    SETTINGS = Settings()
    STORAGE = Storage()
    SEARCH = Search()
    HELP = HelpPage()
