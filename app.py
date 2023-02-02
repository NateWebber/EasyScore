from moviepy.editor import *
from pytube import YouTube
import os
import shutil
import requests

DOWNLOAD_FOLDER = "dl"  # name of the directory for storing downloaded files

"""
Collect image, either from internet or local file
"""
image_source_choice = ""
while (not ((image_source_choice == "1") or (image_source_choice == "2"))):
    image_source_choice = input(
        "Choose 1 for local (file) image, choose 2 to use a URL: ")

image_clip = None
if (image_source_choice == "1"):
    image_path = input(
        "Input the filename of your image (must be in 'images' directory): ")
    image_clip = ImageClip(f"images/{image_path}")
else:
    if (not os.path.exists(DOWNLOAD_FOLDER)):
        os.mkdir(DOWNLOAD_FOLDER)
    image_url = input("Input the URL for your image: ")
    # store the image's original filename, rather than having to come up with one
    image_file_name = image_url.split("/")[-1]
    print(f"IMAGE_FILE_NAME: {image_file_name}")
    res = requests.get(image_url, stream=True)
    if (res.status_code == 200):
        with open(f"{DOWNLOAD_FOLDER}/{image_file_name}", "wb") as image_file:
            shutil.copyfileobj(res.raw, image_file)
        print(f"{image_file_name} successfully downloaded!")
        image_clip = ImageClip(f"{DOWNLOAD_FOLDER}/{image_file_name}")
    else:
        print("Couldn't retrieve image. Please double check URL and try again.")
        sys.exit(0)

"""
Collect audio, either from YouTube or local file
"""
audio_source_choice = ""
while (not ((audio_source_choice == "1") or (audio_source_choice == "2"))):
    audio_source_choice = input(
        "Choose 1 for local (file) audio, choose 2 for YouTube audio: ")

yt = None
audio_clip = None
if (audio_source_choice == "1"):
    audio_path = input(
        "Input the filename of your audio (must be in 'audio' directory): ")
    audio_clip = AudioFileClip(f"audio/{audio_path}")
else:
    if (not os.path.exists(DOWNLOAD_FOLDER)):
        os.mkdir(DOWNLOAD_FOLDER)
    audio_path = input("Input the YouTube URL of your audio: ")
    yt = YouTube(audio_path)
    video = yt.streams.filter(only_audio=True).first()
    yt_audio = video.download(output_path=DOWNLOAD_FOLDER)
    print(f"SAVED AUDIO PATH: {yt_audio}")
    audio_clip = AudioFileClip(yt_audio)

"""
Set video length, with option to just match audio length, as well as check to ensure video isn't longer than audio length (which causes a crash)
"""
video_length = input(
    "Input video length in seconds (input '0' to match audio length): ")
if (audio_clip.duration < int(video_length)):
    print("Audio is shorter than requested duration, setting to maximum duration")
    video_length = audio_clip.duration
elif (video_length == "0"):
    video_length = audio_clip.duration

output_name = input("Input filename for output: ")

"""
Combine video and audio, and render final video
"""
image_clip.audio = audio_clip
# trim final clip to length as determined above
final_clip = image_clip.set_duration(video_length)
# resize the clip to make it more compact/portable. 800px is an arbitrary choice and will be changeable by the user, but probably only after the GUI is implemented
final_clip = final_clip.resize(width=800)
final_clip.write_videofile(f"{output_name}.mp4", 1)

# allow user to delete downloaded files
if (audio_source_choice == "2" or image_source_choice == "2"):
    delete_downloads = input(
        f"Delete temporary downloads? (can be found in '{DOWNLOAD_FOLDER}' directory) [Y/n]")
    if (not ((delete_downloads == "n") or (delete_downloads == "N"))):
        shutil.rmtree(DOWNLOAD_FOLDER)

print("Your video is done!")
