import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title="hopped up out the bed", width=600, height = 300)

with dpg.window(label="turn my swag on"):
    dpg.add_text("took a look in the mirror")
    dpg.add_button(label="said what's up")
    dpg.add_input_text(label="string", default_value="yeah i'm gettin' money")
    dpg.add_slider_float(label="oh", default_value=0.273, max_value=1)
    
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()