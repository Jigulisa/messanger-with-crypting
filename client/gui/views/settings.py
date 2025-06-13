from dearpygui.dearpygui import *

from gui.views.core import View


class Settings(View):
    @property
    def name(self) -> str:
        return "settings"

    def create(self) -> None:
        self.create_appearance_set()
        self.create_roles_place()

    def create_appearance_set(self):
        add_text("background image")
        add_text("selected None", tag="selected_file_text")
        add_file_dialog(directory_selector=True, show=False,
                        callback=self.on_background, tag="for_background",
                        cancel_callback=self.cancel_callback,
                        width=700, height=400)
        add_button(label="Select", callback=lambda: show_item("for_background"))

        add_text("other's message color")
        add_text("selected None", tag="selected_m2_color")
        add_color_picker(tag="for_m2_color",
                         width=int(get_viewport_client_width() * 0.25),
                         height=int(get_viewport_width() * 0.25))
        add_button(label="Select", callback=self.on_m2_color)

        add_text("your message color")
        add_text("selected None", tag="selected_m1_color")
        add_color_picker(tag="for_m1_color",
                         width=int(get_viewport_client_width() * 0.25),
                         height=int(get_viewport_width() * 0.25))
        add_button(label="Select", callback=self.on_m1_color)

        add_text("panels' color")
        add_text("selected None", tag="selected_panels_color")
        add_color_picker(tag="for_panels_color",
                         width=int(get_viewport_client_width() * 0.25),
                         height=int(get_viewport_width() * 0.25))
        add_button(label="Select", callback=self.on_panels_color)

    def create_roles_place(self):
        add_input_text(label="chat")
        add_input_text(label="new role")

    def fill_in_form(self):
        add_button(label="Fill in form", callback=self.on_form)
    def on_background(self, sender, data):
        file_path = data['file_path_name']
        set_value("selected_file_text", f"selected {file_path.split("\\")[-1]}")

    def on_m2_color(self, sender, data):
        color = get_value("for_m2_color")
        set_value("selected_m2_color", f"selected {color}")

    def on_m1_color(self, sender, data):
        color = get_value("for_m1_color")
        set_value("selected_m1_color", f"selected {color}")

    def on_panels_color(self, sender, data):
        color = get_value("for_panels_color")
        set_value("selected_panels_color", f"selected {color}")

    def on_form(self):
        pass

    def cancel_callback(self, sender, app_data):
        print('Cancel was clicked.')
        print("Sender: ", sender)
        print("App Data: ", app_data)
