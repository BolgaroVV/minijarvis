import json
import sounddevice as sd
import multiprocessing as mp
import queue

from vosk import Model, KaldiRecognizer


def stt_process(modelpath, samplerate, audio_q, text_q, stop_event):
    model = Model(modelpath)
    rec = KaldiRecognizer(model, samplerate)

    def q_callback(indata, _, __, status):
        if not stop_event.is_set():
            audio_q.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=samplerate,
        blocksize=8000,
        device=1,
        dtype="int16",
        channels=1,
        callback=q_callback,
    ):
        while not stop_event.is_set():
            try:
                data = audio_q.get(timeout=0.1)
            except queue.Empty:
                continue

            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result())["text"]
                text_q.put(text)

class STT:
    def __init__(self, modelpath: str = "model", samplerate: int = 16000):
        self.modelpath = modelpath
        self.samplerate = samplerate

        self.audio_q = mp.Queue()
        self.text_q = mp.Queue()
        self.stop_event = mp.Event()

        self.process = mp.Process(
            target=stt_process,
            args=(
                self.modelpath,
                self.samplerate,
                self.audio_q,
                self.text_q,
                self.stop_event,
            ),
            daemon=True,
        )

    def start(self):
        self.process.start()

    def listen(self, executor: callable = None):
        try:
            while True:
                text = self.text_q.get()
                print(text)
                if executor:
                    executor(text)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.stop_event.set()
        if self.process.is_alive():
            self.process.join()