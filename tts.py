from piper import PiperVoice, SynthesisConfig
import sounddevice as sd

def createVoice():
    return PiperVoice.load("voicepacks/ru_RU-ruslan-medium.onnx", "voicepacks/ru_RU-ruslan-medium.onnx.json")

def tts_function(text: str, voice: PiperVoice):
    # syn_config = SynthesisConfig(
    #     volume=0.5,  # half as loud
    #     length_scale=1.0,  # twice as slow
    #     noise_scale=1.0,  # more audio variation
    #     noise_w_scale=1.0,  # more speaking variation
    #     normalize_audio=False, # use raw audio from voice
    # )
    chunks = voice.synthesize(text)
    for chunk in chunks:
        sd.play(chunk.audio_float_array, chunk.sample_rate)
        sd.wait()  # Ждем окончания воспроизведения

# with open('data.txt', 'r', encoding='utf-8') as f:
#     text = f.read()
# voice = createVoice()
# tts_function(text, voice)