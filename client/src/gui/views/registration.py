from dearpygui.dearpygui import (
    add_button,
    add_input_text,
    add_text,
)

from gui.views.core import View


class Registration(View):
    @property
    def name(self) -> str:
        return "registration"

    def create(self) -> None:
        add_text("Hello, explorer!", pos=[200, 50])
        add_input_text()
        add_text("come up with a username")
        add_input_text()
        add_text("come up with a good password")
        add_button(label="have toml file?", callback=self.on_have_toml)

    def cancel_callback(self) -> None: ...
    def on_have_toml(self) -> None: ...
