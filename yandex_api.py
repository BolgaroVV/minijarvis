from yandex_music import Client, Track
from pygame_player import AudioPlayer, controls
from stt import STT
import asyncio
import time
import threading

# 113794712
# 5535519
client = Client('y0__xCpmpWuARje-AYg2_7smhYpIYKyuuCA7_QXlcnhWyFwl22cHw')
client.init()

def get_download_link(track: Track) -> str:
    track_download_info = track.get_download_info(1)[0]
    return track_download_info['direct_link']

def get_album_tracks(album_id: int):
    album = client.albums_with_tracks(album_id)
    album_tracks = album['volumes'][0]
    return album_tracks

def voice_controls(text: str):
    cmd = text.strip().lower()
    if cmd == "следующий":
        player.next()
    elif cmd == "пауза":
        player.pause()
    elif cmd == "вернуть":
        player.resume()
    elif cmd == "старт":
        threading.Thread(
            target=run_load_tracks,
            daemon=True
        ).start()
    # elif cmd.startswith("громкость"):
    #     vol = float(input("Введите значение громкости от 0.0 до 1.0: "))
    #     player.set_volume(vol)      

async def load_tracks():
    for track in get_album_tracks(25713686):
        url = get_download_link(track)
        player.add_to_queue(url, track)

def run_load_tracks():
    asyncio.run(load_tracks())

stt = STT()
stt.start(voice_controls)
player = AudioPlayer()

while True:
    print('working')
    time.sleep(1)