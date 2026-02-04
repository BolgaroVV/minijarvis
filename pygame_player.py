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
        self.queue = Queue(maxsize=5)
        self.current_track = []
        self.next_track = []
        self.history = []
        self.back_history = []
        self.running = True

        self.lock = threading.Lock()

        self.worker_thread = threading.Thread(
            target=self._player_worker, daemon=True
        )
        self.worker_thread.start()

    def play(self, next_track):
        if self.current_track:
            self.history.append(self.current_track)
            if len(self.history) > 5:
                self.history = self.history[1:]

        bio = io.BytesIO(next_track[0])
        pygame.mixer.music.load(bio)
        pygame.mixer.music.play()
        self.current_track = next_track
        print("▶️ Воспроизведение:", self.current_track[1]['title'])

    def previous(self):
        with self.lock:
            if not self.history:
                print("⏮ Предыдущего трека нет")
                return
            
            self.back_history.append(self.current_track)
            if len(self.back_history) > 5:
                self.back_history = self.back_history[1:]
            self.current_track = None

            self.play(self.history.pop())
            
    def pause(self):
        pygame.mixer.music.pause()
        self.isPaused = True

    def resume(self):
        pygame.mixer.music.unpause()
        self.isPaused = False

    def next(self):
        if self.back_history:
            self.play(self.back_history.pop())
        else:
            pygame.mixer.music.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def add_to_queue(self, url, track):

        response = requests.get(url)
        response.raise_for_status()
        wav_bytes = response.content
        self.queue.put([wav_bytes, track])

    def _player_worker(self):
        while self.running:
            if not pygame.mixer.music.get_busy() and self.isPaused == False:
                with self.lock:
                    if self.next_track:
                        if self.back_history:
                            self.play(self.back_history.pop())
                        else:
                            self.play(self.next_track)
                            self.next_track = None
                    if not self.queue.empty():
                        self.next_track = self.queue.get()

            time.sleep(0.1)

    def clear_queue(self):
        with self.lock:
            while not self.queue.empty():
                self.queue.get()
        print("🗑 Очередь очищена")
    
    def shutdown(self):
        self.running = False
        pygame.mixer.music.stop()
        pygame.mixer.quit()