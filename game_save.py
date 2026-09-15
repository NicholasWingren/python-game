import json
from types import SimpleNamespace as Namespace

class GameEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__
        
class GameSave:    
    def save_game(self, data):
        file = open("game.txt", "w")
        game_json_data = json.dumps(data, indent=4, cls=GameEncoder)
        file.write(game_json_data)  # write the serialized data to the file
        file.close()
        
    def load_game(self):
        file = open("game.txt", "r")
        serialized_data = file.read()  # read the serialized data from the file
        file.close()
        return json.loads(serialized_data, object_hook=lambda d: Namespace(**d))