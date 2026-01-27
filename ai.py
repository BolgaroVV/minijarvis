import ollama

def response_to_ai(msg: str):
    response = ollama.chat(model='gemma3:1b', messages=[
    {
        'role': 'user',
        'content': msg + 'do not use emoji',
    },
    ])
    return response.message.content