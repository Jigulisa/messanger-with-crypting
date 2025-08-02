from pathlib import Path
from typing import Self
from settings import Settings
from dearpygui.dearpygui import (
    add_button,
    add_color_picker,
    add_file_extension,
    add_input_text,
    add_text,
    file_dialog,
    get_value,
    get_viewport_client_width,
    get_viewport_width,
    set_value,
    show_item,
)

from gui.views.core import View

class Search(View):
    @property
    def name(self: Self) -> str:
        return "search"
    
    def create(self: Self) -> None:
        self.user_name_input = add_input_text(label="who u search for")
        self.search_button = add_button(label = "search!", callback=self.on_search_buttoning)
        
    def on_search_buttoning(self) -> None:
        Settings.add_chat(get_value(self.user_name_input))