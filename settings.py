import json

class Settings:
    def __init__(self):
        with open("settings.json", "r") as f:
            jsondata = json.loads(f.read())
        
        self.token = str(jsondata["token"])
        self.pointer = str(jsondata["pointer"])
        self.cmd = str(jsondata["cmd"])
        self.prefix = str(jsondata["prefix"])
        self.remove_pointer = str(jsondata["remove_pointer"])
        self.option_pointer = str(jsondata["option_pointer"])