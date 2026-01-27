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
        self.current_track = None
        self.next_track = None
        self.running = True

        self.lock = threading.Lock()

        self.worker_thread = threading.Thread(
            target=self._player_worker, daemon=True
        )
        self.worker_thread.start()

    def play(self, bio):
        pygame.mixer.music.load(bio)
        pygame.mixer.music.play()
        self.current_track = bio
        print("▶️ Воспроизведение:", bio)

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

    def add_to_queue(self, url):
        response = requests.get(url)
        response.raise_for_status()
        wav_bytes = response.content
        bio = io.BytesIO(wav_bytes)
        self.queue.put(bio)

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

def controls(player: AudioPlayer):
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

# player = AudioPlayer(volume=0.7)
# player.add_to_queue("https://api.music.yandex.net/get-mp3/f8c23aac883050227eff649ddc5d488e/19bff537d88/U2FsdGVkX1-5lJmL5h0gogm2kb1An3foWXcq7ogFzD1Rnm4sH6T1aYSK7amx-HC_TDV0rR0eq9YkoLwxt_XKCttspB5yIH0JCZ1cLxEmAgktgf0kjESuisO_0HJVYpt3bs_O_KodFfPann1_KLY_VTRz3iN7gCS2kyaD2PlRMjkepfdB0b6cC3XL8tk4fxUtv7Jemt3kPwnQdQQndM1rNkKtbfXEyaCSr-xxBNYv0eQ3G938MROTYmjxn6LLm_PxHuaXFNXJbPHDgCpgp5aOU_qlRv-5Y6m8Kley0MS_qD1eeyMqnrlW0d8VWZip9BZHtAVJPMpyvyJivoU7CmJj10NlyXOA80iVRXIfY7VOGoy2UTdyR3A4ocTdCUaalJl6yC5-fwAKVC9qQMt4As1DOdcGrzkrVHPzunlDAlFlwT9p5EimYYKaJBib6OERBgQJOzKhIijcW5GtIfKbfYYtqehHR7ijgFdvyEEwWBnIHv5H8ibcHUz6qyl8xl11PoOhZz9F_LZT7gnqPNxbTY51NCELglJHe8DFdUV3B3cWDOPIZa5Hl6CQvdHIwaX3oFxCldmRYwymmBsB7Q5WPkgPrSh878HJCuc8dg3DSWBoa2JQipgIT0G61OeQIEV-vFib8HLYZgwDpW4hBJfEWYso0IVU9xCToYRoTvoX2BlYKeq47F7f18i5A3wl03nvnWypeN-k5nnXahfA_-CdQqKkoFPYPFL9jLl_y8OI1KeWqHW20Qs_AUJXkvoTaEuRysAQxc92YdpmlQrj-4ZcZSDQkiiMJG49145VaSkp-jV6xDfRUx97-vya1JLtvgv-ingHIQSH8ge_gNT7d1Z4ctqYBDOrpBr-WLsRzktykFXvtepOgGVQ0wMlMQ370ym2NJvo465F8Nbd1sXFzp-35chPJsEZq14py6pcDU7qpyyQWAEBn_B5TsMJBJEVSVB35QSoK2pIvLShAVbSYPFTmBqbiw/d02YoMR4kQDXiiVxRj0DA3J0tF4_KuOSu0bj5hxu214")
# player.add_to_queue("https://api.music.yandex.net/get-mp3/91c46d09517c756d92bedd40822e6301/19bff5a2725/U2FsdGVkX18WR-IRUHkLddFGkV4gyKF3wqXH_hRgky9mfGvVdecZsJq1RUDizpXfmGVAu4YOnySqNsE9hIZAJFIfL7sjcLOE67RzHzp7ip4WATNXGBsODkb1YDr4iIM4cXi76NfxfQ3gfeUeszR1TB2cCapnS6qQJOhXtQCqqj0l7d7q4u7f6FyEzSGRjjvVQGYzzdLmESE7WqtdlNTlHAcOgV5x4_mkxj0lhaoHwBbmuTLM3-oqbDa4-xxnCucBYWvDrh3HB5w6BEPpPpWFvQCJ-yffvOHAWEw8sJ3GcLMK5j5Bl3e5CY8EHgrg-gmlkDMxsAe1GpH9rCKw0wS5aJu0WO5S8uUNhm5X17gF2cZqr--GV7DO14r0k3dHYKlQ0KrX15h6b2-sgtUvax4DBpo8I-OuA3ug2iITgh8vI1KTM9OJOkbzhbkex2ofDDIetZvCqDU5n1lFmUJN8BQpL081HoDfrCKUac-cETY416s8GSdJfO7ubeekkG_N-Tqm2jvurKiOWLv6Zk_DBYaa3emPwOuwVNAkRe_wmUBd08GGDLfWz3V_o-euhGfv_Z7jVZv34CSg-EnT3A9BFalUCkVr2MBc3JQEIxSCOLusLjvz1xaD-vu3xKmMidO9NU27T2y-rMQvLMuosNLnWOAihG63b8h5DlQzQ_AOJ9zAv64sd9_0jJO8G22QhnCz8CqtsvFOTK4c8wuZ6_97wqeIfHdJ7SIRzUPiJBbyT-7euLEY_t9pVuinoTPL2-5Ljt5SDWhwcn2HwRcfgiEV7giu0Zpy41NuRffSZmeS9wg3RejuirNSuFuEEOJ4JLEOxNZ8-Srrx5Riqv0Tz8cJBY81NZFyrMaNtRabMD8oGRjTFMFFzFVmUrt76g8GoAZGz2U6aNUaeum6zwynbwrC4ON7kZF7sfYLLnNUu1TEH6u8j3q26_dxiPqEMuRPhrig53Tm6vWqzv_Pp_2j15qQtHoI9g/VtbcZhnZ9OQrxGfML-xdS7DZQ_B9UA6Mnw6ubjzNJyU")
# player.add_to_queue("https://api.music.yandex.net/get-mp3/8a66a60bac0d19c5550cb0ec5739b253/19bff5a4c3b/U2FsdGVkX1_Ip5LNsFWbQkeodEI-aYVcc5UgSbCk424eradtovWkWAqN2DzDoADINcp_IT6MHJamKX4DR-T-FjywCq6nMi-oRTTg2IvjncMEiAazIVaZPj-VEQWIbZpfFGSgZmbUuKcTg2gD7BBootD5__85VCzAtTYtYb5Dj-bkR34jLDcJcqaKUBsYfQYFrkxV8bR0Fe15py5IDDC0g4-rlJ0SCm3d6RJaQZahav0S6NzT8D-00JubqNXJDbjBq0ChLNYSVmX3JjDQtn4WJiU-dVXiRWdihcXCNLZvYi-Lx8tgh86VchG0OKRBdNj8oQH746TBxJJJWy96ey7AOhegSdkyBVF6LJKbmq_UxsKo562E7BE9QhyKwyMI074dKIMM1YWyr90DOi0dcTMfpow2uvGaAJcI4-tVqkNv2mC-u7EUBarmimFhEKgeAO3EU6aZEPyctR_gDJIz40F4zpIGBfMEMUFIoUV8uxvOy8QK_ZcT9y1XUh18asNybGx6sWk0-BV3CtBvyU0K-14JODXwcBY2QVrEe4l268IonReBOgBk9TLA2M3puSPuP50a8O5QrzaHZ3SnbUnSREGzn6aMkcD33R8nGtwKaIXZRs2OJyUsHImBMvCwQ75MRxlTY_s04V0IZf8k-8lQihPFnO0XjpDW6-dk3fxgw0NCM78DS8CrDR-sXZga0eg4wxfn752Qpa34svdgIZ4h3po2In5PH-Xsm5QRiwQfPz7Dld-Lr-5dOQzuvZShOBflWRX3e9-Y7JxP4JOZNkHfdbpalz8MsOxXxNWeeOdMgEwP_WlfvWlcsxFzIPISsjJAf7r7wZeeQPONgyWCLOiwBLntg4qOZaJ6NDyq8EonRE9_ubMKFoCFIJHRtLkawk596DzsBLH9IrXL15i00cCx8dfVAOlwXlso01Yi3plA3K4le8OiudaBDS8mbTFV9HuDcQuxPYpacZjbJXl9eBdOcybVvw/iq6BLuqNUT2bXGnoW35k9R31USWshj5xLWMGUyrflZQ")


