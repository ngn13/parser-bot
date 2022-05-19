import json

class Settings:
    def __init__(self):
        with open("settings.json", "r") as f:
            jsondata = json.loads(f.read())
        
        self.token = jsondata["token"]
        self.pointer = jsondata["pointer"]
        self.cmd = jsondata["cmd"]
        self.prefix = jsondata["prefix"]
        self.remove_pointer = jsondata["remove_pointer"]