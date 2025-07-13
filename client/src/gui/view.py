from typing import override

from dearpygui.dearpygui import hide_item, show_item, window

from gui.mixins import ResizeMixin
from gui.views.view_name import ViewName


class View(ResizeMixin):
    @property
    def name(self) -> str:
        return "view"

    @override
    def resize(self, width: int, height: int, position: tuple[int, int]) -> None:
        super().resize(width, height, position)
        ViewName.CHAT.value.resize(width, height)

    def __init__(self) -> None:
        with window(
            label=self.name,
            tag=self.name,
            min_size=(0, 0),
            no_resize=True,
            no_title_bar=True,
            no_move=True,
        ):
            self.create_views()
        self.show_view(ViewName.CHAT)

    def show_view(self, view_name: ViewName) -> None:
        for view in ViewName:
            hide_item(view.value.name)
        show_item(view_name.value.name)

    def create_views(self) -> None:
        for view in ViewName:
            view.value.create_view()
