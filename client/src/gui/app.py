from contextlib import suppress
from queue import Empty, Queue
from dearpygui.dearpygui import (
    create_context,
    create_viewport,
    destroy_context,
    get_viewport_client_height,
    get_viewport_client_width,
    is_dearpygui_running,
    render_dearpygui_frame,
    setup_dearpygui,
    show_viewport,
)
from gui.views.view_name import ViewName
from gui.menu import Menu
from gui.view import View


class Messenger:
    def __init__(
        self,
        width: int,
        height: int,
        queue_send: Queue,
        queue_receive: Queue,
    ) -> None:
        create_context()
        create_viewport(
            title="Cryptogramm",
            width=width,
            height=height,
            min_width=0,
            min_height=0,
        )

        self.width = 0
        self.height = 0
        ViewName.CHAT.value.queue_send = queue_send
        self.view = View()
        self.menu = Menu(callback=self.view.show_view)
        self.queue_receive = queue_receive
        setup_dearpygui()
        show_viewport()

    def resize(self, width: int, height: int) -> None:
        self.menu.resize(
            width=width // 4,
            height=height,
            position=(0, 0),
        )
        self.view.resize(
            width=width - width // 4,
            height=height,
            position=(width // 4, 0),
        )
        self.width = width
        self.height = height

    def run(self) -> None:
        while is_dearpygui_running():
            width = get_viewport_client_width()
            height = get_viewport_client_height()

            if width != self.width or height != self.height:
                self.resize(width, height)
            with suppress(Empty):
                ViewName.CHAT.value.on_receiving(self.queue_receive.get_nowait())
            render_dearpygui_frame()

        destroy_context()
