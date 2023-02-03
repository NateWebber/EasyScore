from enum import Enum


class ImageSource(Enum):
    LOCAL = 0
    INET_URL = 1


class AudioSource(Enum):
    LOCAL = 0
    YOUTUBE = 1
