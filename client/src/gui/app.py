from collections.abc import Callable
from contextlib import suppress
from queue import Empty, Queue
from re import compile

from dearpygui.dearpygui import (
    add_button,
    add_font_range_hint,
    add_input_text,
    add_text,
    add_window,
    bind_font,
    create_context,
    create_viewport,
    delete_item,
    destroy_context,
    does_item_exist,
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
    window,
)

from gui.menu import Menu
from gui.view import View
from gui.views.view_name import ViewName
from settings.storage import Storage


class SignIn:
    def __init__(self) -> None:
        self.pattern = compile(
            r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}$",
        )
        create_context()

        create_viewport(width=300, height=200)
        self.password = None
        self.main_window = add_window(
            label="Cryptogram",
            width=290,
            height=220,
            no_title_bar=True,
            no_resize=True,
            no_move=True,
            pos=[-1, -1],
        )

        with (
            font_registry(),
            font(str(Storage.base_dir / "fonts" / "font.otf"), 20) as default_font,
        ):
            add_font_range_hint(mvFontRangeHint_Default)
            add_font_range_hint(mvFontRangeHint_Cyrillic)
            bind_font(default_font)

        add_text("Hello again, explorer!", parent=self.main_window)
        self.password_input = add_input_text(
            default_value="your password",
            parent=self.main_window,
        )
        add_button(label="Continue", callback=self.on_password, parent=self.main_window)
        setup_dearpygui()
        show_viewport()
        start_dearpygui()
        destroy_context()

    def make_notification(self, message: str) -> None:
        if does_item_exist("Notification"):
            delete_item("Notification")
        with window(
            tag="Notification",
            width=300,
            height=250,
            no_resize=True,
            pos=[0, 0],
        ):
            add_text(message, wrap=290)
            add_button(
                label="Ok",
                callback=lambda: delete_item("Notification"),
            )

    def on_password(self) -> None:
        password: str = get_value(self.password_input)
        is_correct = bool(self.pattern.match(password))
        if is_correct:
            self.password = password
            stop_dearpygui()
        else:
            self.make_notification(
                "Oops, wrong password. It must contain at least"
                "8 characters, 1 small letter, 1 big letter and a number",
            )


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
            min_width=260,
            min_height=400,
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
