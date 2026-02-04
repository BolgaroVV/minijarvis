from yandex_music import Track, Album
import asyncio
import threading
from services import container

class MusicControls():
    def __init__(self):
        self._load_id = 0
        self._lock = threading.Lock()
        self.thread = None
        self.stop_event = threading.Event()
    def start_loader(self, loader, *args):
        print(threading.active_count())
        print(threading.enumerate())
        def wrapper():     
            with self._lock:
                loader(*args)
        self.thread = threading.Thread(target=wrapper, daemon=True)
        self.thread.start()

    # Получение информации по текущему треку
    @property
    def _current_track(self):
        return container.player.current_track[1]
    
    def _current_track_info(self):
        return container.client.tracks(self._current_track['id'])[0]

    def _current_album(self):
        return self._current_track_info()['albums'][0]['id']
    
    def _current_artists(self):
        return [artist['id'] for artist in self._current_track_info()['artists']]
    
    # Контроллеры плеера без привязки к текущему треку
    def play_next_track(self):
        container.player.next()
    def pause_player(self):
        container.player.pause()
    def resume_player(self):
        container.player.resume()
    def start_player(self):
        self.start_loader(self.play_chart)
    def play_previous_track(self):
        container.player.previous()

    # Лайки дизлайки текущего трека/альбома/артиста
    def like_current_track(self):
        container.client.users_likes_tracks_add(self._current_track['id'])
    def unlike_current_track(self):
        container.client.users_likes_tracks_remove(self._current_track['id'])
    def dislike_current_track(self):
        container.client.users_dislikes_tracks_add(self._current_track['id'])
    def undislike_current_track(self):
        container.client.users_dislikes_tracks_remove(self._current_track['id'])
    def like_current_album(self):
        container.client.users_likes_albums_add(self._current_album())
    def unlike_current_album(self):
        container.client.users_likes_albums_remove(self._current_album())
    def like_current_artist(self):
        container.client.users_likes_artists_add(self._current_artists())
    def unlike_current_artist(self):
        container.client.users_likes_artists_remove(self._current_artists())

    # Добавить трек в конец очереди
    def add_track_to_queue(self, track: Track = container.client.tracks(34608)[0]):
        self.start_loader(lambda: asyncio.run(self.load_track(track)))

    # Включить трек после текущего
    def play_next_track_after_current(self, track: Track = container.client.tracks(34608)[0]):
        self.stop_event.set()
        self.thread.join()  
        container.player.clear_queue()
        self.add_track_to_queue(track)

    # Включить трек прямо сейчас
    def play_track_right_now(self, track: Track = container.client.tracks(34608)[0]):
        self.play_next_track_after_current(track)
        container.player.next()

    
    def get_download_link(self, track: Track) -> str:
        track_download_info = track.get_download_info(1)[0]
        return track_download_info['direct_link']
    def get_album_tracks(self, album_id: int):
        album = container.client.albums_with_tracks(album_id)
        album_tracks = album['volumes'][0]
        return album_tracks
    def play_chart(self):
        chart_info = container.client.chart()
        chart_playlist = chart_info['chart']
        asyncio.run(self.play_playlist(chart_playlist))

    async def play_playlist(self, playlist):
        for short_track in playlist['tracks']:
            if self.stop_event.is_set():
                print('thread cancelled')
                self.stop_event.clear()
                return
            track = short_track['track']
            await self.load_track(track)

    def start_play_album(self):
        self.start_loader(lambda: asyncio.run(self.play_album()))

    async def play_album(self):
        album=self.get_album_tracks(40387457)
        for track in album:
            if self.stop_event.is_set():
                print('thread cancelled')
                return
            await self.load_track(track)

    async def load_track(self, track):
        url = self.get_download_link(track)
        container.player.add_to_queue(url, {'id': track['id'], 'title': track['title']})
        print(f'added {track['title']}')    

    def search_track(self):
        return container.client.search(text='blod tear', type_='track', nocorrect=False)




    