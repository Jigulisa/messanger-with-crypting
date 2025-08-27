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
    get_item_width,
    get_value,
    get_y_scroll_max,
    set_item_height,
    set_item_pos,
    set_item_width,
    set_value,
    set_y_scroll,
    window,
)

from gui.views.core import View
from net.dto import MessageDTO
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
            self.chats = Settings.get_chats()
            for name in self.chats:
                add_button(
                    label=name,
                    tag=name,
                    callback=lambda *, selected_chat=name: self.callback(selected_chat),
                )
            add_button(label="new chat", parent="chats_list")

    def create_personal_zone(self: Self) -> None:
        with child_window(tag="personal_zone"):
            group_id = add_group(horizontal=True)

            add_text("no1", tag="chat_name", parent=group_id)
            add_button(label="+", parent=group_id)

    def create_chat_place(self: Self) -> None:
        with child_window(label="Messages", tag="chat_place", border=False):
            add_group(tag="message_group")

    def create_text_zone(self: Self) -> None:
        with child_window(label="text", tag="text_place"):
            group_id = add_group(horizontal=True)
            add_input_text(
                default_value="☆*:.｡.o(≧▽≦)o.｡.:*☆",
                tag="input",
                width=get_item_width("text_place") - 70,
                parent=group_id,
            )
            add_button(
                label="send",
                callback=lambda: self.on_sending(),
                parent=group_id,
            )

    def callback(self: Self, selected_chat: str) -> None:
        delete_item("message_group", children_only=True)
        set_value("chat_name", selected_chat)
        self.current_chat = selected_chat

    def on_sending(self: Self) -> None:
        inp = get_value("input")
        set_value("input", "")
        self.queue_send.put(
            MessageDTO(
                text=inp,
                sent_time=datetime.now(UTC),
                author=Settings.get_public_key(),
                chat_id=self.current_chat,
                signature="",
            ),
        )

    def on_receiving(self: Self, message: MessageDTO) -> None:
        if not message.is_spam:
            add_text(
                f"{message.author[:6]}: {message.text}",
                parent="message_group",
                wrap=get_item_width("chat_place"),
            )
        else:
            add_button(
                label="SPAM",
                callback=lambda data=message.text: self.on_spam(data),
            )
        set_y_scroll("chat_place", get_y_scroll_max("chat_place") + 25)

    def on_spam(self, text: str) -> None:
        with window(label="SPAM", width=350, height=450, no_resize=True):
            add_text(text, wrap=430)

    def update_chat_list(self) -> None:
        chats = Settings.get_chats()
        delete_item("chats_list", children_only=True)
        add_button(label="new chat", callback=lambda: ..., parent="chats_list")
        for name in chats:
            add_button(
                label=name,
                tag=name,
                callback=lambda *, selected_chat=name: self.callback(selected_chat),
                parent="chats_list",
            )
        self.chats = chats
