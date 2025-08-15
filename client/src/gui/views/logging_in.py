from pathlib import Path

from dearpygui.dearpygui import (
    add_button,
    add_file_extension,
    add_input_text,
    add_text,
    file_dialog,
)

from gui.views.core import View


class LoggingIn(View):
    @property
    def name(self) -> str:
        return "logging in"

    def create(self) -> None:
        add_text("Hello again, explorer!", pos=[200, 50])
        add_input_text()
        add_text("your password")
        with file_dialog(
            directory_selector=False,
            show=False,
            callback=self.on_toml,
            tag="toml_",
            cancel_callback=self.cancel_callback,
            width=700,
            height=400,
            file_count=1,
        ):
            add_file_extension(".toml")
        add_text("upload file")
        add_button(label="no file?", callback=self.on_no_toml)

    def cancel_callback(self) -> None: ...
    def on_no_toml(self) -> None: ...

    def on_toml(
        self,
        _sender: str,
        data: dict[str, str | list[float] | dict[str, str]],
    ) -> None:
        if isinstance(data["selections"], dict):
            self.settings_file = Path(next(iter(data["selections"].values())))
