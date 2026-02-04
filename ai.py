from ollama import chat
from yandex_api import music_controls

model = 'qwen3:1.7b'

def zaglushka():
    print('no function')

avaliable_functions = {
    "play_next_track": music_controls.play_next_track,
    "pause_player": music_controls.pause_player,
    "resume_player": music_controls.resume_player,
    "like_current_track": music_controls.like_current_track,
    "start_player": music_controls.start_player,
    "play_previous_track": music_controls.play_previous_track,
    "like_current_track": music_controls.like_current_track,
    "unlike_current_track": music_controls.unlike_current_track,
    "dislike_current_track": music_controls.dislike_current_track,
    "like_current_album": music_controls.like_current_album,
    "unlike_current_album": music_controls.unlike_current_album,
    "like_current_artist": music_controls.like_current_artist,
    "unlike_current_artist": music_controls.unlike_current_artist,
    "zaglushka": zaglushka
}
ollama_tools = [
    {        
        "type": "function",
        "function": {
            "name": "zaglushka",
            "description": "Используй эту функцию когда нет подоходящих или запрос пустой"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "play_next_track",
            "description": "Включает следующий трек"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "play_previous_track",
            "description": "Включает предыдущий трек"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pause_player",
            "description": "Ставит воспроизведение на паузу"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "resume_player",
            "description": "Продолжает воспроизведение"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "start_player",
            "description": "Запускает плеер"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "like_current_track",
            "description": "Ставит лайк текущему треку"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "unlike_current_track",
            "description": "Убирает лайк с текущего трека"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "dislike_current_track",
            "description": "Ставит дизлайк текущему треку"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "like_current_album",
            "description": "Ставит лайк текущему альбому"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "unlike_current_album",
            "description": "Убирает лайк с текущего альбома"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "like_current_artist",
            "description": "Ставит лайк текущему исполнителю"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "unlike_current_artist",
            "description": "Убирает лайк у текущего исполнителя"
        }
    }
]

def call_function_by_ai(request: str):
  if len(request) < 2:
      print('no request')
      return
  messages = [{"role": "user", "content": request}]
  response = chat(model=model, messages=messages, tools=ollama_tools, think=True)
  if response.message.tool_calls:
      for tool in response.message.tool_calls:
          if function_to_call := avaliable_functions.get(tool.function.name):
              print('calling: ', tool.function.name)
          else:
              print('function', tool.function.name, ' not found')
  else:
      print(response.message.content)
