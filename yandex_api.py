from yandex_music import Client, Track
import json
import urllib.request
from pathlib import Path
from pygame_player import AudioPlayer, controls

# 113794712
# 5535519
client = Client('y0__xCpmpWuARje-AYg2_7smhYpIYKyuuCA7_QXlcnhWyFwl22cHw')
client.init()

# client.accountSettings()
# client.account_status()
# print(client.albums_with_tracks(5535519))
# client.artists_tracks(id)
# client.chart(chart_option='place')
# client.feed()
# client.account_settings_set()

# with open('data.json', 'w') as f:
#     f.write(json.dumps(client.albums_with_tracks(5535519).to_json()))

###### ШТУКА ДЛЯ ЗАГРУЗКИ И УДАЛЕНИЯ ФАЙЛОВ НА ДИСКЕ #######
# def download_track_by_id(id: int):
#     track = client.tracks(id)[0]
#     track_download_info = track.get_download_info(1)[0]
#     urllib.request.urlretrieve(track_download_info['direct_link'], f'{track.id}.{track_download_info['codec']}')
# def delete_track_by_id(id: int):
#     file = Path(f'{id}.mp3')
#     if file.exists():
#         file.unlink()

def get_download_link(track: Track) -> str:
    track_download_info = track.get_download_info(1)[0]
    return track_download_info['direct_link']

def get_album_tracks(album_id: int):
    album = client.albums_with_tracks(album_id)
    album_tracks = album['volumes'][0]
    return album_tracks

player = AudioPlayer()
# controls(player)
for i in get_album_tracks(25713686):
    url = get_download_link(i)
    # print(url)
    player.add_to_queue(url)

try:
    while True:
        cmd = input("Введите команду (next, pause, resume, volume): ").strip().lower()
        if cmd == "next":
            player.next()
        elif cmd == "pause":
            player.pause()
        elif cmd == "resume":
            player.resume()
        elif cmd.startswith("volume"):
            vol = float(input("Введите значение громкости от 0.0 до 1.0: "))
            player.set_volume(vol)  
except KeyboardInterrupt:
    player.shutdown()   