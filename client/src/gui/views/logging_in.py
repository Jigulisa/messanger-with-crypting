from pathlib import Path

from dearpygui.dearpygui import (
    add_button,
    add_file_extension,
    add_input_text,
    add_text,
    file_dialog,
    get_value
)

from gui.views.core import View


class LoggingIn(View):
    @property
    def name(self) -> str:
        return "logging in"

    def create(self) -> None:
        self.password = add_text("Hello again, explorer!", pos=[200, 50])
        add_input_text(default_value="your password", callback=self.on_password)

    def on_password(self) -> None:
        input_text = get_value(self.password)
