from dearpygui.dearpygui import *

from gui.views.core import View


class Chat(View):
    @property
    def name(self) -> str:
        return "chat"

    def resize(self, width: int, height: int) -> None:
        set_item_width("chats_list", width // 4)
        set_item_height("chats_list", height)
        set_item_pos("chats_list", (0, 0))

        set_item_width("personal_zone", width - width // 4)
        set_item_height("personal_zone", height // 10)
        set_item_pos("personal_zone", (width // 4, 0))

        set_item_width("chat_place", width - width // 4)
        set_item_height("chat_place", height - height // 10 * 2)
        set_item_pos("chat_place", (width // 4, height // 10))

        set_item_width("text_place", width - width // 4)
        set_item_height("text_place", height // 10)
        set_item_pos("text_place", (width // 4, height - height // 10))

    def create(self) -> None:
        self.create_list()
        self.create_personal_zone()
        self.create_chat_place()
        self.create_text_zone()

    def create_list(self) -> None:
        with child_window(label="Chats", tag="chats_list"):
            chats = ("andy", "class chagt", "dad", "barotrauma")
            for chat in chats:
                add_button(label=chat, tag=chat, callback=lambda *, sender=chat: self.callback(sender))

    def create_personal_zone(self):
        with child_window(tag="personal_zone"):
            add_text("no1", tag="chat_name")

    def create_chat_place(self) -> None:
        with child_window(label="Messages", tag="chat_place"):
            add_text("chat place lmao")

    def create_text_zone(self) -> None:
        with child_window(label="text", tag="text_place"):
            add_input_text(default_value="☆*:.｡.o(≧▽≦)o.｡.:*☆ ", tag="input")
            add_button(label="send", callback=self.on_sending)

    def callback(self, name_of_chat_epta) -> None:
        delete_item("chat_place", children_only=True)
        with child_window(parent="chat_place"):
            add_text(f"chat with {name_of_chat_epta}")
        set_value("chat_name", name_of_chat_epta)

    def on_sending(self, sender, data):
        inp = get_value("input")
        set_value("input", "")
        print(inp)  # replace with sending to server
