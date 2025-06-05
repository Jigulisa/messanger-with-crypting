# import dearpygui.dearpygui as dpg
#
# WIDTH = 1280  # here was tkinter
# HEIGHT = 720
#
# dpg.create_context()
# dpg.create_viewport(title='Messanger', width=WIDTH // 2, height=HEIGHT // 2)
#
# with dpg.window(label="Messanger", width=dpg.get_viewport_width() // 2,
#                 height=dpg.get_viewport_height() - 39, tag="messanger", no_title_bar=True):
#     dpg.add_text("School chat")
#     dpg.add_button(label="Send", )
#     dpg.add_input_text(label="ur message", default_value="bobr curwa")
#     dpg.add_slider_float(label="sm settings", default_value=0.853, max_value=1)
# previous_size = (dpg.get_viewport_width(), dpg.get_viewport_height())
#
#
# def resize_handler():
#     width, height = dpg.get_viewport_width(), dpg.get_viewport_height()
#     if previous_size != (width, height):
#         dpg.configure_item("messanger", width=width // 2, height=height - 39)
#
#
# dpg.setup_dearpygui()
# dpg.show_viewport()
# while dpg.is_dearpygui_running():
#     resize_handler()
#     dpg.render_dearpygui_frame()
#
# dpg.start_dearpygui()
# dpg.destroy_context()

import dearpygui.dearpygui as dpg

WIDTH, HEIGHT = 1280, 720


class MessengerApp:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window_tags = ["chats_list", "chat_messages"]
        self.sizes = [(4, 1, "0", "0"), (1.36, 1.2, "self.width // 4 - 1", "self.height // 15")]
        self.previous_size = (width, height)
        dpg.create_context()
        dpg.create_viewport(title='Solorous', width=self.width, height=self.height)
        self.create_windows()
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def create_windows(self):
        for i in range(len(self.window_tags)):
            with dpg.window(width=self.width // self.sizes[i][0], height=self.height // self.sizes[i][1],
                            tag=self.window_tags[i], no_title_bar=True, no_move=True):
                dpg.set_item_pos(self.window_tags[i], [eval(self.sizes[i][2]), eval(self.sizes[i][3])])
                if self.window_tags[i] == "chats_list":
                    for j in ["andy", "class chat", "mom", "barotrauma"]:  # here data should be taken from db
                        dpg.add_text(j)
                if self.window_tags[i] == "chat_messages":
                    dpg.add_text("hi")
                    dpg.add_text("hello")

                    dpg.add_input_text(label="ur message", default_value="bobr curwa")
                    dpg.add_button(label="Send")

    def refactor_windows(self):
        self.width = dpg.get_viewport_width()
        self.height = dpg.get_viewport_height()
        if self.previous_size != (self.width, self.height):
            for i in range(len(self.window_tags)):
                dpg.configure_item(self.window_tags[i], width=self.width // self.sizes[i][0],
                                   height=self.height // self.sizes[i][1])
                dpg.set_item_pos(self.window_tags[i], [eval(self.sizes[i][2]), eval(self.sizes[i][3])])

            self.previous_size = (self.width, self.height)

    def run(self):
        while dpg.is_dearpygui_running():
            self.refactor_windows()
            dpg.render_dearpygui_frame()
        dpg.destroy_context()


if __name__ == "__main__":
    app = MessengerApp(WIDTH, HEIGHT)
    app.run()
