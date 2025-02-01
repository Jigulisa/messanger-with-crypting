import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = dpg.add_font("NotoSerifCJKjp-Medium.otf", 20)
    second_font = dpg.add_font("NotoSerifCJKjp-Medium.otf", 10)

with dpg.window(label="Font Example", height=200, width=200):
    dpg.add_button(label="Default font")
    b2 = dpg.add_button(label="Secondary font")
    dpg.add_button(label="default")

    # set font of specific widget
    dpg.bind_font(default_font)
    dpg.bind_item_font(b2, second_font)

dpg.show_font_manager()

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()


def save_callback():
    print("Save Clicked")


dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.window(label="Example Window"):
    dpg.add_text("Hello world")
    dpg.add_button(label="Save", callback=save_callback)
    dpg.add_input_text(label="string")
    dpg.add_slider_float(label="float")

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
