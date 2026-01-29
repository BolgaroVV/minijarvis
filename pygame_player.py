import pygame
import threading
import time
from queue import Queue
import requests
import io

class AudioPlayer:
    def __init__(self, volume=0.5):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(volume)

        self.isPaused = False
        self.queue = Queue()
        self.current_track = []
        self.next_track = []
        self.running = True

        self.lock = threading.Lock()

        self.worker_thread = threading.Thread(
            target=self._player_worker, daemon=True
        )
        self.worker_thread.start()

    def play(self, next_track):
        pygame.mixer.music.load(next_track[0])
        pygame.mixer.music.play()
        self.current_track = next_track
        print("▶️ Воспроизведение:", self.current_track[1])

    def pause(self):
        pygame.mixer.music.pause()
        self.isPaused = True

    def resume(self):
        pygame.mixer.music.unpause()
        self.isPaused = False

    def next(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def add_to_queue(self, url, track):
        response = requests.get(url)
        response.raise_for_status()
        wav_bytes = response.content
        bio = io.BytesIO(wav_bytes)
        self.queue.put([bio, track['title']])

    def _player_worker(self):
        while self.running:
            if not pygame.mixer.music.get_busy() and self.isPaused == False:
                with self.lock:
                    if self.next_track:
                        self.play(self.next_track)
                        self.next_track = None
                    if not self.queue.empty():
                        self.next_track = self.queue.get()

            time.sleep(0.1)

    def shutdown(self):
        self.running = False
        pygame.mixer.music.stop()
        pygame.mixer.quit()