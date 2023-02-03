from moviepy.editor import *
from pytube import YouTube
import pytube.exceptions
from es_enums import AudioSource, ImageSource
import os
import shutil
import requests


class Renderer:
    DOWNLOAD_FOLDER = "dl"  # name of the directory for storing downloaded files

    image_source_type = ImageSource.INET_URL
    image_source_path = ""
    audio_source_type = AudioSource.YOUTUBE
    audio_source_path = ""

    video_length = 15
    output_name = "out"

    def __init__(self, new_img_type, new_img_source, new_audio_type, new_audio_source, new_vid_length, new_out_name="out"):
        self.image_source_type = new_img_type
        self.image_source_path = new_img_source
        self.audio_source_type = new_audio_type
        self.audio_source_path = new_audio_source
        self.video_length = new_vid_length
        self.output_name = new_out_name
        # self.render()

    def render(self):
        image_clip = None
        audio_clip = None

        # prepare image clip
        match(self.image_source_type):
            case ImageSource.LOCAL:
                image_clip = self.fetch_image_local()
            case ImageSource.INET_URL:
                image_clip = self.fetch_image_url()
            case _:
                print(
                    f"Error: encountered unexpected image source type {self.image_source_type}")

        if image_clip == None:
            return ("Error retrieving image. Double check URL and try again.")
        if type(image_clip) == str:
            return image_clip

        # prepare audio clip
        match(self.audio_source_type):
            case AudioSource.LOCAL:
                audio_clip = self.fetch_audio_local()
            case AudioSource.YOUTUBE:
                audio_clip = self.fetch_audio_youtube()
            case _:
                print(
                    f"Error: encountered unexpected audio source type {self.audio_source_type}")

        if audio_clip == None:
            return ("Error retrieving audio. Double check URL and try again.")
        if type(audio_clip) == str:
            return audio_clip
        

        # trim and render
        if (audio_clip.duration < int(self.video_length)):
            print("Audio is shorter than requested duration, setting to maximum duration")
            self.video_length = audio_clip.duration

        image_clip.audio = audio_clip
        final_clip = image_clip.set_duration(self.video_length)
        final_clip = final_clip.resize(width=800)
        final_clip.write_videofile(f"{self.output_name}.mp4", 1)
        return "OK"

    def fetch_image_url(self) -> ImageClip:
        if (not os.path.exists(self.DOWNLOAD_FOLDER)):
            os.mkdir(self.DOWNLOAD_FOLDER)

        # store the image's original filename, rather than having to come up with one
        image_file_name = self.image_source_path.split("/")[-1]
        print(f"IMAGE_FILE_NAME: {image_file_name}")

        try:
            res = requests.get(self.image_source_path, stream=True)
        except requests.exceptions.MissingSchema:
            return ("Invalid image URL. Please double check URL and try again.")

        if (res.status_code == 200):
            with open(f"{self.DOWNLOAD_FOLDER}/{image_file_name}", "wb") as image_file:
                shutil.copyfileobj(res.raw, image_file)
            print(f"{image_file_name} successfully downloaded!")
            return ImageClip(f"{self.DOWNLOAD_FOLDER}/{image_file_name}")
        else:
            print("Couldn't retrieve image. Please double check URL and try again.")

    def fetch_audio_youtube(self) -> AudioClip:
        if (not os.path.exists(self.DOWNLOAD_FOLDER)):
            os.mkdir(self.DOWNLOAD_FOLDER)
        try:
            yt = YouTube(self.audio_source_path)
        except pytube.exceptions.RegexMatchError:
            return "Invalid YouTube URL. Please double check URL and try again."
        video = yt.streams.filter(only_audio=True).first()
        yt_audio = video.download(output_path=self.DOWNLOAD_FOLDER)
        print(f"SAVED AUDIO PATH: {yt_audio}")

        return AudioFileClip(yt_audio)

    def fetch_image_local(self) -> ImageClip:
        return ImageClip(self.image_source_path)

    def fetch_audio_local(self) -> AudioClip:
        return AudioFileClip(self.audio_source_path)
