from dearpygui.dearpygui import hide_item, show_item, window

from gui.mixins import ResizeMixin
from gui.views.view_name import ViewName


class View(ResizeMixin):
    def __init__(self, name: str) -> None:
        self.name = name
        with window(
            label=name,
            tag=name,
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
