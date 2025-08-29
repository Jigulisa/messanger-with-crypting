from pathlib import Path
from typing import Self

from dearpygui.dearpygui import (
    add_button,
    add_checkbox,
    add_color_picker,
    add_file_extension,
    add_input_int,
    add_input_text,
    add_radio_button,
    add_text,
    file_dialog,
    get_value,
    get_viewport_client_width,
    get_viewport_width,
    set_value,
    show_item,
    window,
)

from gui.views.core import View


class Settings(View):
    @property
    def name(self: Self) -> str:
        return "settings"

    def create(self: Self) -> None:
        add_text("Settings")
        self.create_appearance_set()
        self.new_username_place()
        self.fill_in_form()

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

    def new_username_place(self: Self) -> None:
        self.new_username = add_input_text(default_value="your new username")
        add_button(label="ok", callback=self.on_new_username)
        self.is_spam_tracker_on = add_radio_button(label="Spam tracker",
                                                   callback=self.spam_tracker_switch)

    def spam_tracker_switch(self) -> None:
        if get_value(self.is_spam_tracker_on):
            pass
    def on_new_username(self) -> None:
        pass
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
        with window(tag="form", width=700, label="Self Form"):
            add_text("ФИО")
            add_input_text()
            add_text("Gender")
            add_radio_button(items=["male", "female", "ламинат"], horizontal=True)
            add_text("Age")
            add_input_int()
            add_text("Hobbies")
            add_checkbox(label="voleyball")
            add_checkbox(label="programming")
            add_checkbox(label="ML")
            add_checkbox(label="algorythms")
            add_checkbox(label="rock music")
            add_checkbox(label="drawing")
            add_checkbox(label="art")
            add_checkbox(label="manga")
            add_checkbox(label="anime")
            add_checkbox(label="politics")
            add_checkbox(label="DIY")
            add_checkbox(label="style")
            add_checkbox(label="hairstyling")
            add_checkbox(label="knitting")
            add_checkbox(label="series")
            add_checkbox(label="frontend")
            add_checkbox(label="doing music")
            add_checkbox(label="reading")
            add_checkbox(label="other")

            add_button(label="Save!", callback=self.on_form_saving)

    def cancel_callback(self: Self) -> None: ...

    def on_form_saving(self: Self) -> None: ...
