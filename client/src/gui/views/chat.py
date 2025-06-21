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
                add_button(
                    label=chat,
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
            add_button(label="send", callback=lambda: self.on_new_message)

    def callback(self, name_of_chat_epta) -> None:
        delete_item("chat_place", children_only=True)
        with child_window(parent="chat_place"):
            add_text(f"chat with {name_of_chat_epta}")
        set_value("chat_name", name_of_chat_epta)

    async def on_sending(self):
        inp = await get_value("input")
        set_value("input", "")
        add_text(inp, parent="message_group")
        set_value("message_input", "")
        set_y_scroll("chat_child", get_y_scroll_max("chat_child") + 25)


    async def on_receiving(self):
        inp = await

    async def on_new_message(self):
        while True:
            await self.on_sending()
            await self.on_receiving()
