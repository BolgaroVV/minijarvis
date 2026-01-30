from ollama import chat
from tts import tts_function, createVoice
import threading
import queue

voice = createVoice()

stream = chat(
  model='qwen3:1.7b',
  messages=[{'role': 'user', 'content': 'Сделай текст длиной в 1000 слов, не используй эмоджи и ии ответы'}],
  stream=True,
  think=True
)

tts_queue = queue.Queue()
STOP = object()

def tts_worker():
    while True:
        text = tts_queue.get()
        if text is STOP:
            break
        tts_function(text, voice)
        tts_queue.task_done()

threading.Thread(target=tts_worker, daemon=True).start()

content = ""
isWas = False

for chunk in stream:
    print(chunk.message.content, end="", flush=True)
    content += chunk.message.content
    if '. ' in content and len(content.split()) > 6 and not isWas:
        tts_queue.put(content[:content.find('. ') -1])
        isWas = True

if content.strip():
    tts_queue.put(content[content.find('. '):])

tts_queue.join()
tts_queue.put(STOP)