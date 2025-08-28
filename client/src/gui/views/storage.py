from dearpygui.dearpygui import (
    add_button,
    add_group,
    add_input_text,
    add_text,
    delete_item,
    does_item_exist,
    get_item_children,
    get_item_label,
    get_value,
    window,
)

from gui.views.core import View
from net.storage import (
    delete_file,
    download_file,
    get_file_names,
    get_file_properties,
    rename,
)
from settings import storage


class Storage(View):
    @property
    def name(self) -> str:
        return "storage"

    def create(self) -> None:
        add_text("Storage")
        self.file_names = get_file_names()
        self.file_names = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
        ]

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
            add_button(
                label="properties",
                width=285,
                height=30,
                callback=lambda data=file_name: self.on_propertying(data),
            )
            add_button(
                label="delete file",
                width=285,
                height=30,
                callback=lambda data=file_name: self.on_deleting(data),
            )
            add_button(
                label="close",
                callback=lambda: delete_item(f"second_window_{name}"),
                width=285,
                height=30,
            )

    def on_downloading(self, name: str) -> None:
        data = download_file(name)
        if data:
            with (storage.Storage.base_dir / "downloads" / name).open("wb") as file:
                file.write(data)
            self.make_notification(f"File {name} was downloaded!")
        else:
            self.make_notification("An exception has caused. File was not downloaded.")

    def resize(self, width: int, height: int) -> None:
        delete_item("storage", children_only=True)
        add_text("Storage", parent="storage")
        if self.file_names:
            row_size = width // 110
            if row_size == 0:
                row_size += 1
            self.file_group_ids = [
                add_group(horizontal=True, parent="storage")
                for _ in range(
                    len(self.file_names) // row_size + 1,
                )
            ]
            for fn in self.file_names:
                for group in self.file_group_ids:
                    if len(get_item_children(group)[1]) < row_size:
                        add_button(
                            label=fn,
                            width=100,
                            height=100,
                            callback=self.on_tapping,
                            parent=group,
                        )
                        break

    def on_newnaming(self, file_name: str) -> None:
        with window(width=200, height=200, no_resize=True):
            add_input_text(label="Enter new name", tag="new_name")
            add_button(
                label="Ok",
                callback=lambda data=file_name: self.button_callback(data),
            )

    def button_callback(self, old: str) -> None:
        new = get_value("new_name")
        self.make_notification(rename(old, new))

    def on_propertying(self, file_name: str) -> None:
        props = get_file_properties(file_name)
        with window(
            tag="File properties",
            label="File properties",
            width=300,
            height=450,
            no_resize=True,
        ):
            for i, j in props:
                add_text(f"{i}: {j}", wrap=290)

    def make_notification(self, message: str) -> None:
        with window(
            tag="Notification",
            width=300,
            height=150,
            no_resize=True,
        ):
            add_text(message, wrap=290)
            add_button(
                label="Ok",
                callback=lambda data="Notification": delete_item(data),
            )

    def on_deleting(self, file_name: str) -> None:
        result = delete_file(file_name)
        self.make_notification(result)
