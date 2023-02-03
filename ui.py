import dearpygui.dearpygui as dpg
from renderer import Renderer
from es_enums import AudioSource, ImageSource


def render_video():
    selected_image_path = None
    selected_image_source = None
    selected_audio_path = None
    selected_audio_source = None

    print(f"image tabs value: {dpg.get_value('ui_image_tabs')}")
    match dpg.get_value("ui_image_tabs"):
        case "ui_image_tab_internet":
            selected_image_path = dpg.get_value("input_image_remote_url")
            selected_image_source = ImageSource.INET_URL
        case "ui_image_tab_local":
            selected_image_path = dpg.get_file_dialog_info(
                "input_image_local_file")['file_path_name']
            selected_image_source = ImageSource.LOCAL

    match dpg.get_value("ui_audio_tabs"):
        case "ui_audio_tab_youtube":
            selected_audio_path = dpg.get_value("input_audio_remote_url")
            selected_audio_source = AudioSource.YOUTUBE
        case "ui_audio_tab_local":
            selected_audio_path = dpg.get_file_dialog_info(
                "input_audio_local_file")['file_path_name']
            selected_audio_source = AudioSource.LOCAL

    renderer = Renderer(selected_image_source, selected_image_path,
                        selected_audio_source, selected_audio_path, dpg.get_value("input_video_duration"))
    renderer.render()
    print("Rendering complete!")


dpg.create_context()
dpg.create_viewport(title='EasyScore', width=600, height=600)

# Main Window
with dpg.window(tag="Main"):
    # Image Section
    with dpg.collapsing_header(label="Image", default_open=True):
        with dpg.tab_bar(tag="ui_image_tabs"):
            # Internet Tab
            with dpg.tab(label="Internet", tag="ui_image_tab_internet"):
                dpg.add_input_text(label="Image URL",
                                   tag="input_image_remote_url")
            # Local Tab
            with dpg.tab(label="Local", tag="ui_image_tab_local"):
                dpg.add_button(label="Select an image file", tag="ui_open_image_file_dialog",
                               callback=lambda: dpg.show_item("input_image_local_file"))
                with dpg.file_dialog(directory_selector=False, tag="input_image_local_file", show=False, width=500, height=300):
                    dpg.add_file_extension(
                        "Image files (*.png *.jpg *.bmp){.png,.jpg,.bmp}")

    # Audio Section
    with dpg.collapsing_header(label="Audio", default_open=True):
        with dpg.tab_bar(tag="ui_audio_tabs"):
            # Youtube Tab
            with dpg.tab(label="YouTube", tag="ui_audio_tab_youtube"):
                dpg.add_input_text(label="Youtube URL",
                                   tag="input_audio_remote_url")
            # Local Tab
            with dpg.tab(label="Local", tag="ui_audio_tab_local"):
                dpg.add_button(label="Select an audio file", tag="ui_open_audio_file_dialog",
                               callback=lambda: dpg.show_item("input_audio_local_file"))
                with dpg.file_dialog(directory_selector=False, tag="input_audio_local_file", show=False, width=500, height=300):
                    dpg.add_file_extension(
                        "Audio files (*.mp3 *.wav *.ogg){.mp3,.wav,.ogg}")

    # Options/Extras Section
    with dpg.collapsing_header(label="Options/Extras", default_open=True):
        dpg.add_text("Extra stuff here")
        # "options/extras" will include:
        # video length (may need to reconsider max value in future)
        dpg.add_input_int(label="Video Duration (seconds)",
                          default_value=15, min_value=0, max_value=9999, tag="input_video_duration")
        # choosing where audio starts from
        # choosing to delete downloads after process is complete
        # other things that i'm forgetting at the moment

    # Run Section
    with dpg.collapsing_header(label="Run", default_open=True):
        dpg.add_button(label="Run", callback=render_video, width=250, height=50)
        dpg.add_text("Eventually status text goes here", tag="ui_status_text")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
