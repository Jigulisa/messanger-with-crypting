from dearpygui.dearpygui import (
    add_text,
    add_button,
    does_item_exist,
    delete_item,
    window)

from gui.views.core import View
from net.storage import get_file_names

class Storage(View):
    @property
    def name(self) -> str:
        return "storage"

    def create(self) -> None:
        self.file_names = get_file_names()
        for fn in self.file_names:
            add_button(label=fn, width=100, height=100, callback=self.on_tapping)
    
    def on_tapping(self):
        with window(tag="second_window", label="More...", width=300, height=300, no_title_bar=True):
            add_button(label="download")
            add_button(label="change name")
            add_button(label="properties")
            add_button(label="delete file")
            add_button(label="close", callback=lambda: delete_item("second_window"))


