from dearpygui.dearpygui import (
    add_button,
    add_text,
    delete_item,
    does_item_exist,
    get_item_label,
    window,
)

from gui.views.core import View
from net.storage import get_file_names


class Storage(View):
    @property
    def name(self) -> str:
        return "storage"

    def create(self) -> None:
        # with font_registry():
        #     self.font = add_font("font.otf", 20)
        #     add_font_range_hint(mvFontRangeHint_Cyrillic)
        #     add_font_range_hint(mvFontRangeHint_Default)
        self.file_names = get_file_names()
        for fn in self.file_names:
            add_button(label=fn, width=100, height=100, callback=self.on_tapping)
        # bind_font(font)

    def on_tapping(self, name: str):
        if does_item_exist(f"second_window_{name}"):
            delete_item(f"second_window_{name}")
        self.menu = window(
            tag=f"second_window_{name}",
            width=300,
            height=300,
            no_title_bar=True,
            no_resize=True,
        )
        with self.menu:
            add_text(default_value=str(get_item_label(name)))
            add_button(label="download", width=285, height=30)
            add_button(label="change name", width=285, height=30)
            add_button(label="properties", width=285, height=30)
            add_button(label="delete file", width=285, height=30)
            add_button(
                label="close",
                callback=lambda: delete_item(f"second_window_{name}"),
                width=285,
                height=30,
            )
