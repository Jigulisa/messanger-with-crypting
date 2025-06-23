from dearpygui.dearpygui import *
from datetime import datetime, UTC
from queue import Queue
from gui.views.core import View
from net.message_struct import ReceivedPrivateMessage, SentPrivateMessage
from settings import Settings


class Chat(View):
    def __init__(self):
        self.queue_send = Queue()
        self.current_chat = ""

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
                add_button(
                    label=chat[:6],
                    tag=chat,
                    callback=lambda *, sender=chat: self.callback(sender),
                )

    def create_personal_zone(self):
        with child_window(tag="personal_zone"):
            add_text("no1", tag="chat_name")

    def create_chat_place(self) -> None:
        with child_window(label="Messages", tag="chat_place", border=False):
            add_group(tag="message_group")

    def create_text_zone(self) -> None:
        with child_window(label="text", tag="text_place"):
            add_input_text(default_value="☆*:.｡.o(≧▽≦)o.｡.:*☆", tag="input")
            add_button(label="send", callback=lambda: self.on_sending())

    def callback(self, name_of_chat_epta) -> None:
        delete_item("chat_place", children_only=True)
        set_value("chat_name", name_of_chat_epta[:6])
        self.current_chat = name_of_chat_epta

    def on_sending(self):
        print("evrrev")
        inp = get_value("input")
        set_value("input", "")
        self.queue_send.put(
            SentPrivateMessage(
                message=inp,
                sent_time=datetime.now(UTC),
                author=Settings.get_public_key(),
                recieve_id=self.current_chat,
                signature=""
            )
        )

    def on_receiving(self, message: ReceivedPrivateMessage):
        add_text(f"{message.author[:6]}: {message.message}", parent="message_group")
        set_y_scroll("chat_child", get_y_scroll_max("chat_child") + 25)
