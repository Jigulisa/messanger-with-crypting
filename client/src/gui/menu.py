from collections.abc import Callable

from dearpygui.dearpygui import add_button, window

from gui.mixins import ResizeMixin
from gui.views.view_name import ViewName


class Menu(ResizeMixin):
    @property
    def name(self) -> str:
        return "menu"

    def __init__(self, callback: Callable[[ViewName], None]) -> None:
        with window(
            label=self.name,
            tag=self.name,
            min_size=(0, 0),
            no_resize=True,
            no_title_bar=True,
            no_move=True,
        ):
            self.create_menu(callback)

    def create_menu(self, callback: Callable[[ViewName], None]) -> None:
        for view in ViewName:
            add_button(
                label=view.value.name,
                tag=f"button_{view.value.name}",
                callback=lambda *, v=view: callback(v),
            )
