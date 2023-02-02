from moviepy.editor import * 

clip = ImageClip("images/meme.jpg")
audio_clip = AudioFileClip("audio/metal.mp3")

clip.audio = audio_clip

clip = clip.set_duration(10)

clip.write_videofile("test.mp4", 1) 