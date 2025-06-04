import dearpygui.dearpygui as dpg

WIDTH = 1280  # here was tkinter
HEIGHT = 720

dpg.create_context()
dpg.create_viewport(title='Messanger', width=WIDTH // 2, height=HEIGHT // 2)

with dpg.window(label="Messanger", width=dpg.get_viewport_width() // 2,
                height=dpg.get_viewport_height(), tag="messanger"):
    dpg.add_text("School chat")
    dpg.add_button(label="Send", )
    dpg.add_input_text(label="ur message", default_value="bobr curwa")
    dpg.add_slider_float(label="sm settings", default_value=0.853, max_value=1)


def resize_handler():
    width, height = dpg.get_viewport_width(), dpg.get_viewport_height()
    dpg.configure_item("messanger", width=width // 2, height=height)


dpg.setup_dearpygui()
dpg.show_viewport()
while dpg.is_dearpygui_running():
    resize_handler()
    dpg.render_dearpygui_frame()

dpg.start_dearpygui()
dpg.destroy_context()
