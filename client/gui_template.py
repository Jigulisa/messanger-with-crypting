import dearpygui.dearpygui as dpg

WIDTH = 1280  # here was tkinter
HEIGHT = 720

dpg.create_context()
dpg.create_viewport(title='Messanger', width=WIDTH // 2, height=HEIGHT // 2)

with dpg.window(label="Messanger", width=dpg.get_viewport_width() // 2,
                height=dpg.get_viewport_height() - 39, tag="messanger", no_title_bar=True):
    dpg.add_text("School chat")
    dpg.add_button(label="Send", )
    dpg.add_input_text(label="ur message", default_value="bobr curwa")
    dpg.add_slider_float(label="sm settings", default_value=0.853, max_value=1)
previous_size = (dpg.get_viewport_width(), dpg.get_viewport_height())


def resize_handler():
    width, height = dpg.get_viewport_width(), dpg.get_viewport_height()
    if previous_size != (width, height):
        dpg.configure_item("messanger", width=width // 2, height=height - 39)


dpg.setup_dearpygui()
dpg.show_viewport()
while dpg.is_dearpygui_running():
    resize_handler()
    dpg.render_dearpygui_frame()

dpg.start_dearpygui()
dpg.destroy_context()
