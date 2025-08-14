import pathlib

from dearpygui.dearpygui import (
    add_button,
    add_input_text,
    add_text,
    delete_item,
    does_item_exist,
    get_item_label,
    get_value,
    window,
)

from gui.views.core import View
from net.storage import download_file, rename


class Storage(View):
    @property
    def name(self) -> str:
        return "storage"

    def create(self) -> None:
        self.file_names = ["3", "4"]
        for fn in self.file_names:
            add_button(label=fn, width=100, height=100, callback=self.on_tapping)

    def on_tapping(self, name: str) -> None:
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
            file_name = str(get_item_label(name))
            add_text(default_value=file_name)
            add_button(
                label="download",
                width=285,
                height=30,
                callback=lambda data=file_name: self.on_downloading(data),
            )
            add_button(
                label="change name",
                width=285,
                height=30,
                callback=lambda data=file_name: self.on_newnaming(data),
            )
            add_button(label="properties", width=285, height=30)
            add_button(label="delete file", width=285, height=30)
            add_button(
                label="close",
                callback=lambda: delete_item(f"second_window_{name}"),
                width=285,
                height=30,
            )

    def on_downloading(self, name: str) -> None:
        data = download_file(name)
        if data:
            path = pathlib.Path().parent.parent.parent.parent.as_posix()
            with open(path + name, "wb") as f:
                f.write(data)
            with window(
                tag="Notification",
                width=300,
                height=150,
                no_resize=True,
            ):
                add_text(f"File {name} was downloaded!", wrap=290)
                add_button(
                    label="Ok",
                    callback=lambda data="Notification": delete_item(data),
                )
        else:
            with window(
                tag="Notification",
                width=300,
                height=150,
                no_resize=True,
            ):
                add_text("An exception has caused. File was not downloaded.", wrap=290)
                add_button(label="Ok")

    def on_newnaming(self, file_name: str) -> None:
        with window(width=200, height=200, no_resize=True):
            add_input_text(label="Enter new name", tag="new_name")
            add_button(
                label="Ok",
                callback=lambda data=file_name: self.button_callback(data),
            )

    def button_callback(self, old: str) -> None:
        new = get_value("new_name")
        rename(old, new)
