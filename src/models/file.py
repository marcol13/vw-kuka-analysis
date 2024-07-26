import json

class DataFile:
    def __init__(self, path):
        self.path = path

    def read(self) -> any:
        with open(self.path, 'r') as f:
            return json.load(f)

    def write(self, data, directory='.') -> None:
        with open(f"{directory}/{self.path}.json", 'w') as f:
            json.dump(data, f)

            

