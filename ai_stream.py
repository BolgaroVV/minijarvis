from ollama import chat

stream = chat(
  model='qwen3:1.7b',
  messages=[{'role': 'user', 'content': 'Сделай текст длиной в 1000 слов, не используй эмоджи и ии ответы'}],
  stream=True,
  think=True
)

for chunk in stream:
    print(chunk.message.content, end="", flush=True)
    content += chunk.message.content
