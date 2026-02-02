import json
import queue
import sounddevice as sd
import threading
import time

from vosk import Model, KaldiRecognizer

class STT:
    def __init__(self, modelpath: str = "model", samplerate: int = 16000):
        self.model = Model(modelpath)
        self.__REC__ = KaldiRecognizer(self.model, samplerate)
        self.__Q__ = queue.Queue()
        self.__SAMPLERATE__ = samplerate
        self._running = True
    
    def q_callback(self, indata, _, __, status):
        self.__Q__.put(bytes(indata))

    def listen(self, executor: callable = None):
        with sd.RawInputStream(
                samplerate=self.__SAMPLERATE__, 
                blocksize=8000, 
                device=1, 
                dtype='int16',
                channels=1, 
                callback=self.q_callback
            ):
            while self._running:
                data = self.__Q__.get()
                if self.__REC__.AcceptWaveform(data):
                    text = json.loads(self.__REC__.Result())["text"]
                    print(text)
                    if executor:
                        executor(text)
                # else:
                #     text = json.loads(self.__REC__.PartialResult())["partial"] - возможно полезно для wakewords и всяких ключевых

    def start(self, executor: callable = None):
        threading.Thread(
            target=self.listen,
            args=(executor,),
            daemon=True
        ).start()

    def stop(self):
        self._running = False

# stt = STT()
# stt.start()

# while True:
#     print('working')
#     time.sleep(1)