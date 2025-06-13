from dearpygui.dearpygui import *
from enum import Enum
from gui.views.core import View


class Chat(View):
    @property
    def name(self) -> str:
        return "chat"

    def create(self) -> None:
        self.create_list()
        self.create_chat_place()
        self.create_text_zone()
        self.create_personal_zone()

    def create_list(self) -> None:
        with child_window(label="Chats", width=get_viewport_client_width() // 4,
                          pos=(0, 0),
                          tag="chats_list"):
            chats = ("andy", "class chagt", "dad", "barotrauma")
            for chat in chats:
                add_button(label=chat, tag=chat, callback=lambda f="sm1": self.callback(f, "chat_place"))

    def create_chat_place(self) -> None:
        with child_window(label="Messages", width=get_viewport_client_width() * 0.5,
                          height=get_viewport_client_height() * 0.65,
                          pos=(get_viewport_client_width() * 0.25, get_viewport_client_height() * 0.1),
                          tag="chat_place"):
            add_text("chat place lmao")

    def create_text_zone(self) -> None:
        with child_window(label="text", width=get_viewport_client_width() * 0.5,
                          height=get_viewport_client_height() * 0.1,
                          pos=(get_viewport_client_width() * 0.25, get_viewport_client_height() * 0.73),
                          tag="text_place"):
            add_input_text(default_value="☆*:.｡.o(≧▽≦)o.｡.:*☆ ", tag="input")
            add_button(label="send", callback=self.on_sending)

    def create_personal_zone(self):
        with child_window(width=get_viewport_client_width() * 0.5, height=get_viewport_client_height() * 0.1,
                          pos=(get_viewport_client_width() // 4, 0), tag="personal_zone"):
            add_text("no1", tag="chat_name")

    def callback(self, name, parent) -> None:
        delete_item(parent, children_only=True)
        with child_window(width=get_viewport_client_width() * 0.5,
                          height=get_viewport_client_width(),
                          parent=parent, pos=(0, 0)):
            add_text(f"chat with {name}")
        set_value("chat_name", name)

    def on_sending(self, sender, data):
        inp = get_value("input")
        set_value("input", "")
        print(inp)  # replace with sending to server
