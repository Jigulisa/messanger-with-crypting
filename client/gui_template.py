import dearpygui.dearpygui as dpg
import tkinter as tk

root = tk.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
root.destroy()

dpg.create_context()
dpg.create_viewport(title='Messanger', width=WIDTH // 2, height=HEIGHT // 2)

with dpg.window(label="Messanger", width=WIDTH//4, height=HEIGHT//2):
    dpg.add_text("School chat")
    dpg.add_button(label="Send",)
    dpg.add_input_text(label="ur message", default_value="bobr curwa")
    dpg.add_slider_float(label="sm settings", default_value=0.853, max_value=1)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
