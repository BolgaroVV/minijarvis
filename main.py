import json
from sst import sst_recorder
from ai import response_to_ai
from tts import createVoice, tts_function
from wav_player import wav_player

voice = createVoice()

sst_result = sst_recorder()
print(sst_result)
json_sst_result = json.loads(sst_result)['text']
print(json_sst_result)
ai_result = response_to_ai(json_sst_result)
print(ai_result)
tts_function(ai_result, voice)
wav_player()


