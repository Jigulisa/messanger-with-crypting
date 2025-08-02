from datetime import UTC, datetime
from queue import Queue
from typing import Self

from dearpygui.dearpygui import (
    add_button,
    add_group,
    add_input_text,
    add_text,
    child_window,
    delete_item,
    get_value,
    get_y_scroll_max,
    set_item_height,
    set_item_pos,
    set_item_width,
    set_value,
    set_y_scroll,
)

from gui.views.core import View
from net.message_struct import ReceivedPrivateMessage, SentPrivateMessage
from settings import Settings


class Chat(View):
    def __init__(self: Self) -> None:
        self.queue_send = Queue()
        self.current_chat = ""

    @property
    def name(self: Self) -> str:
        return "chat"

    def resize(self: Self, width: int, height: int) -> None:
        set_item_width("chats_list", width // 4)
        set_item_height("chats_list", height)
        set_item_pos("chats_list", [0, 0])

        set_item_width("personal_zone", width - width // 4)
        set_item_height("personal_zone", height // 10)
        set_item_pos("personal_zone", [width // 4, 0])

        set_item_width("chat_place", width - width // 4)
        set_item_height("chat_place", height - height // 10 * 2)
        set_item_pos("chat_place", [width // 4, height // 10])

        set_item_width("text_place", width - width // 4)
        set_item_height("text_place", height // 10)
        set_item_pos("text_place", [width // 4, height - height // 10])

    def create(self: Self) -> None:
        self.create_list()
        self.create_personal_zone()
        self.create_chat_place()
        self.create_text_zone()

    def create_list(self: Self) -> None:
        with child_window(label="Chats", tag="chats_list"):
            chats = Settings.get_chats() 
            for chat in chats:
                add_button(
                    label=chat[:6],
                    tag=chat,
                    callback=lambda *, sender=chat: self.callback(sender),
                )

    def create_personal_zone(self: Self) -> None:
        with child_window(tag="personal_zone"):
            add_text("no1", tag="chat_name")

    def create_chat_place(self: Self) -> None:
        with child_window(label="Messages", tag="chat_place", border=False):
            add_group(tag="message_group")

    def create_text_zone(self: Self) -> None:
        with child_window(label="text", tag="text_place"):
            add_input_text(default_value="☆*:.｡.o(≧▽≦)o.｡.:*☆", tag="input")
            add_button(label="send", callback=lambda: self.on_sending())

    def callback(self: Self, selected_chat: str) -> None:
        delete_item("message_group", children_only=True)
        set_value("chat_name", selected_chat[:6])
        self.current_chat = selected_chat

    def on_sending(self: Self) -> None:
        inp = get_value("input")
        set_value("input", "")
        self.queue_send.put(
            SentPrivateMessage(
                message=inp,
                sent_time=datetime.now(UTC),
                author=Settings.get_public_key(),
                receive_id=self.current_chat,
                signature="",
            ),
        )

    def on_receiving(self: Self, message: ReceivedPrivateMessage) -> None:
        add_text(f"{message.author[:6]}: {message.message}", parent="message_group")
        set_y_scroll("chat_place", get_y_scroll_max("chat_place") + 25)
    
    def update_chat_list(self):
        delete_item("chats_list")
        with child_window(label="Chats", tag="chats_list", parent="view"):
            chats = Settings.get_chats() 
            for chat in chats:
                add_button(
                    label=chat[:6],
                    tag=chat,
                    callback=lambda *, sender=chat: self.callback(sender)
                )
        
