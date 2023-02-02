from moviepy.editor import *
from pytube import YouTube
import os
import shutil

image_path = input("Input the filename of your image (must be in 'images' directory): ")
clip = ImageClip(f"images/{image_path}")

audio_source_choice = 0
while (not ((audio_source_choice == "1") or (audio_source_choice == "2"))):
    audio_source_choice = input("Choose 1 for local (file) audio, choose 2 for YouTube audio: ")

yt = None
audio_clip = None
if (audio_source_choice == "1"):
    audio_path = input("Input the filename of your audio (must be in 'audio' directory): ")
    audio_clip = AudioFileClip(f"audio/{audio_path}")
else:
    audio_path = input("Input the YouTube URL of your audio: ")
    yt = YouTube(audio_path)
    video = yt.streams.filter(only_audio=True).first()
    if (not os.path.exists("temp")):
        os.mkdir("temp")
    yt_audio = video.download(output_path="temp")
    print(f"SAVED AUDIO PATH: {yt_audio}")
    audio_clip = AudioFileClip(yt_audio)

video_length = input("Input video length (in seconds): ")
if (audio_clip.duration < int(video_length)):
    print("Audio is shorter than requested duration, setting to maximum duration")
    video_length = audio_clip.duration

output_name = input("Input filename for output: ")

clip.audio = audio_clip

clip = clip.set_duration(video_length).resize(width=800)

clip.write_videofile(f"{output_name}.mp4", 1)

if (audio_source_choice == "2"):
    delete_downloads = input("Delete temporary downloads? (can be found in 'temp' directory) [Y/n]")
    if (not ((delete_downloads == "n") or (delete_downloads == "N"))):
        shutil.rmtree("temp")
    
