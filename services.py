from pygame_player import AudioPlayer
from stt import STT
from yandex_music import Client
import os
from dotenv import load_dotenv
load_dotenv()

YANDEX_TOKEN = os.getenv("YANDEX_MUSIC_TOKEN")

if not YANDEX_TOKEN:
    raise ValueError("Токен Yandex Music не найден! Добавьте его в .env")

class Container:
    player = AudioPlayer()
    stt = STT()
    client = Client(YANDEX_TOKEN)

container = Container()
