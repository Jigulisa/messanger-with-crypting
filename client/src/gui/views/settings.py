from pathlib import Path
from typing import Self

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


class Settings(View):
    @property
    def name(self: Self) -> str:
        return "settings"

    def create(self: Self) -> None:
        self.create_appearance_set()
        self.create_roles_place()

    def create_appearance_set(self: Self) -> None:
        add_text("background image")
        add_text("selected None", tag="selected_file_text")
        with file_dialog(
            directory_selector=False,
            show=False,
            callback=self.on_background,
            tag="for_background",
            cancel_callback=self.cancel_callback,
            width=700,
            height=400,
            file_count=1,
        ):
            add_file_extension(".*")
        add_button(label="Select", callback=lambda: show_item("for_background"))

        add_text("other's message color")
        add_text("selected None", tag="selected_m2_color")
        add_color_picker(
            tag="for_m2_color",
            width=int(get_viewport_client_width() * 0.25),
            height=int(get_viewport_width() * 0.25),
        )
        add_button(label="Select", callback=self.on_m2_color)

        add_text("your message color")
        add_text("selected None", tag="selected_m1_color")
        add_color_picker(
            tag="for_m1_color",
            width=int(get_viewport_client_width() * 0.25),
            height=int(get_viewport_width() * 0.25),
        )
        add_button(label="Select", callback=self.on_m1_color)

        add_text("panels' color")
        add_text("selected None", tag="selected_panels_color")
        add_color_picker(
            tag="for_panels_color",
            width=int(get_viewport_client_width() * 0.25),
            height=int(get_viewport_width() * 0.25),
        )
        add_button(label="Select", callback=self.on_panels_color)

    def create_roles_place(self: Self) -> None:
        add_input_text(label="chat")
        add_input_text(label="new role")

    def fill_in_form(self: Self) -> None:
        add_button(label="Fill in form", callback=self.on_form)

    def on_background(
        self: Self,
        _sender: str,
        data: dict[str, str | list[float] | dict[str, str]],
    ) -> None:
        if isinstance(data["selections"], dict):
            file = Path(next(iter(data["selections"].values())))
            set_value("selected_file_text", f"selected {file.name}")

    def on_m2_color(self: Self) -> None:
        color = get_value("for_m2_color")
        set_value("selected_m2_color", f"selected {color}")

    def on_m1_color(self: Self) -> None:
        color = get_value("for_m1_color")
        set_value("selected_m1_color", f"selected {color}")

    def on_panels_color(self: Self) -> None:
        color = get_value("for_panels_color")
        set_value("selected_panels_color", f"selected {color}")

    def on_form(self: Self) -> None:
        pass

    def cancel_callback(self: Self) -> None:
        pass
