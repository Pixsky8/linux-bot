import json

class Config:

    token = ""
    prefix = ""
    strings = 0

    def __init__(self):
        fsett = open("config/settings.json")
        data = json.load(fsett)
        self.token = data["token"]
        self.prefix = data["prefix"]
        fsett.close()
