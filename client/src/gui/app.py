from collections.abc import Callable
from contextlib import suppress
from queue import Empty, Queue

from dearpygui.dearpygui import (
    add_button,
    add_font_range_hint,
    add_input_text,
    add_text,
    add_window,
    bind_font,
    create_context,
    create_viewport,
    destroy_context,
    font,
    font_registry,
    get_value,
    get_viewport_client_height,
    get_viewport_client_width,
    is_dearpygui_running,
    mvFontRangeHint_Cyrillic,
    mvFontRangeHint_Default,
    render_dearpygui_frame,
    set_exit_callback,
    set_viewport_resize_callback,
    setup_dearpygui,
    show_viewport,
    start_dearpygui,
    stop_dearpygui,
)

from gui.menu import Menu
from gui.view import View
from gui.views.view_name import ViewName
from settings.storage import Storage


class SignIn:
    def __init__(self) -> None:
        create_context()
        create_viewport()
        self.password = None
        self.main_window = add_window(label="Cryptogram")
        with (
            font_registry(),
            font(str(Storage.base_dir / "fonts" / "font.otf"), 20) as default_font,
        ):
            add_font_range_hint(mvFontRangeHint_Default)
            add_font_range_hint(mvFontRangeHint_Cyrillic)
            bind_font(default_font)

        add_text("Hello again, explorer!", pos=[200, 50], parent=self.main_window)
        self.password_input = add_input_text(
            default_value="your password",
            parent=self.main_window,
        )
        add_button(label="Continue", callback=self.on_password, parent=self.main_window)
        setup_dearpygui()
        show_viewport()
        start_dearpygui()
        destroy_context()

    def on_password(self) -> None:
        self.password = get_value(self.password_input)
        stop_dearpygui()


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

        with (
            font_registry(),
            font(str(Storage.base_dir / "fonts" / "font.otf"), 20) as default_font,
        ):
            add_font_range_hint(mvFontRangeHint_Default)
            add_font_range_hint(mvFontRangeHint_Cyrillic)
            bind_font(default_font)

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
        start_dearpygui()

        while is_dearpygui_running():
            with suppress(Empty):
                ViewName.CHAT.value.on_receiving(self.queue_receive.get_nowait())
            render_dearpygui_frame()
        destroy_context()
