import json
from yandex_api import MusicControls

music_controls = MusicControls()

with open('controls_dict.json', 'r', encoding='utf-8') as f:
    command_config = json.load(f)

function_registry = {
    "play_next_track": music_controls.play_next_track,
    "pause_player": music_controls.pause_player,
    "resume_player": music_controls.resume_player,
    "like_current_track": music_controls.like_current_track,
    "start_player": music_controls.start_player,
    "play_previous_track": music_controls.play_previous_track
}

def execute_command(command_name):
    if command_name not in command_config:
        print(f"Неизвестная команда: {command_name}")
        return None
    
    config = command_config[command_name]
    func_name = config["function"]
    
    if func_name not in function_registry:
        print(f"Функция {func_name} не зарегистрирована")
        return None
    
    return function_registry[func_name]()