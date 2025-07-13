from collections.abc import Callable
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
    set_exit_callback,
    set_viewport_resize_callback,
    setup_dearpygui,
    show_viewport,
)

from gui.menu import Menu
from gui.view import View
from gui.views.view_name import ViewName


class Messenger:
    def __init__(
        self,
        width: int,
        height: int,
        queue_send: Queue,
        queue_receive: Queue,
        exit_callback: Callable[[], None],
    ) -> None:
        create_context()
        create_viewport(
            title="Cryptogramm",
            width=width,
            height=height,
            min_width=0,
            min_height=0,
        )
        set_exit_callback(exit_callback)
        set_viewport_resize_callback(self.resize)

        ViewName.CHAT.value.queue_send = queue_send
        self.view = View()
        self.menu = Menu(callback=self.view.show_view)
        self.queue_receive = queue_receive
        setup_dearpygui()
        show_viewport()

    def resize(self) -> None:
        width = get_viewport_client_width()
        height = get_viewport_client_height()

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

    def run(self) -> None:
        while is_dearpygui_running():
            with suppress(Empty):
                ViewName.CHAT.value.on_receiving(self.queue_receive.get_nowait())
            render_dearpygui_frame()
        destroy_context()
