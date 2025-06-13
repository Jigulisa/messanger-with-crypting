from dearpygui.dearpygui import add_text

from gui.views.core import View


class Storage(View):
    @property
    def name(self) -> str:
        return "storage"

    def create(self) -> None:
        add_text("SSSSSTTTTOOOOORRRRRRRAAAAAAAAAAAAAAAAAGEEEEEEEEEEEEEE")
