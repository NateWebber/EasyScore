from moviepy.editor import * 

image_path = input("Input the filename of your image (must be in 'images' directory): ")
audio_path = input("Input the filename of your audio (must be in 'audio' directory): ")
video_length = input("Input video length (in seconds): ")
output_name = input("Input filename for output: ")

clip = ImageClip(f"images/{image_path}")
audio_clip = AudioFileClip(f"audio/{audio_path}")

clip.audio = audio_clip

clip = clip.set_duration(video_length).resize(width=800)

clip.write_videofile(f"{output_name}.mp4", 1)