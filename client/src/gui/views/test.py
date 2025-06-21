import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(label="Chat Example", width=400, height=300):
    with dpg.child_window(tag="chat_child", width=-1, height=200, border=True):
        dpg.add_group(tag="message_group")
    dpg.add_input_text(tag="message_input", width=-1, on_enter=True)
    dpg.add_button(label="Send", callback=lambda: send_message())

def send_message():
    global last_message
    msg = dpg.get_value("message_input")
    if not msg:
        return
    # Добавляем новое сообщение
    item = dpg.add_text(msg, parent="message_group")
    dpg.set_value("message_input", "")
    # Скроллим вниз
    dpg.set_y_scroll("chat_child", dpg.get_y_scroll_max("chat_child") + 25)


dpg.create_viewport(title='Dear PyGui Chat', width=420, height=350)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
