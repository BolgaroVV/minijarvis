import wave
from piper import PiperVoice

def createVoice():
    return PiperVoice.load("voicepacks/ru_RU-ruslan-medium.onnx")

def tts_function(text: str, voice: PiperVoice):
    with wave.open("test.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)