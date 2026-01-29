import ollama

def response_to_ai(msg: str):
    response = ollama.chat(model='qwen3:1.7b', messages=[
    {
        'role': 'user',
        'content': msg + 'do not use emoji',
    },
    ])
    return response.message.content