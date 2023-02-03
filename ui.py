import dearpygui.dearpygui as dpg
from renderer import Renderer
from es_enums import AudioSource, ImageSource

"""
Gather user-input parameters and pass them to the "backend" to run the rendering process
"""


def render_video():
    renderer = Renderer(ImageSource.INET_URL, dpg.get_value("input_image_remote_url"),
                        AudioSource.YOUTUBE, dpg.get_value("input_audio_remote_url"), dpg.get_value("input_video_duration"))
    renderer.render()
    print("did i do it?")


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
        dpg.add_input_int(label="Video Duration (seconds)",
                          default_value=15, min_value=0, max_value=9999, tag="input_video_duration")
        # choosing where audio starts from
        # choosing to delete downloads after process is complete
        # other things that i'm forgetting at the moment

    with dpg.collapsing_header(label="Run", default_open=True):
        dpg.add_button(label="Run", callback=render_video)
        dpg.add_text("Eventually status text goes here", tag="ui_status_text")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
