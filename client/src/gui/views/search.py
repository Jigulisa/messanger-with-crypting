from typing import Self

from dearpygui.dearpygui import add_button, add_input_text, add_text, get_value

from gui.views.core import View
from net.chat import create_chat
from settings import Settings


class Search(View):
    @property
    def name(self: Self) -> str:
        return "search"

    def create(self: Self) -> None:
        self.user_name_input = add_input_text(label="who u search for")
        self.search_button = add_button(
            label="search!",
            callback=self.on_search_buttoning,
        )
        self.recommend_people_text = add_text("people we recommend to u")

    def on_search_buttoning(self) -> None:
        name = get_value(self.user_name_input)
        uuid = create_chat(name)
        if uuid is not None:
            Settings.add_chat(name, uuid)
