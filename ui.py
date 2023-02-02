import dearpygui.dearpygui as dpg

"""
Gather user-input parameters and pass them to the "backend" to run the rendering process
"""


def render_video():
    print("someday I will actually render the video")


dpg.create_context()
dpg.create_viewport(title='EasyScore', width=600, height=600)

with dpg.window(tag="Main"):
    with dpg.collapsing_header(label="Image", default_open=True):
        with dpg.tab_bar():
            with dpg.tab(label="Internet"):
                dpg.add_input_text(label="Image URL",
                                   tag="input_image_remote_url")
            with dpg.tab(label="Local"):
                dpg.add_text("Select an image file")

    with dpg.collapsing_header(label="Audio", default_open=True):
        with dpg.tab_bar():
            with dpg.tab(label="YouTube"):
                dpg.add_input_text(label="Youtube URL",
                                   tag="input_audio_remote_url")
            with dpg.tab(label="Local"):
                dpg.add_text("Select an audio file")

    with dpg.collapsing_header(label="Options/Extras", default_open=False):
        dpg.add_text("Extra stuff here")
        # "options/extras" will include:
        # video length
        # choosing where audio starts from
        # choosing to delete downloads after process is complete
        # other things that i'm forgetting at the moment

    with dpg.collapsing_header(label="Run", default_open=True):
        dpg.add_button(label="Run", callback=render_video)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
