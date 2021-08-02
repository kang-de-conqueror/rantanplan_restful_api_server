import json

class Config:

    def __init__(self):
        return

    @staticmethod
    def load_config():
        f = open("config.json")
        data = json.load(f)
        return data

    @staticmethod
    def get_connection_string():
        return Config.load_config().get("CONNECTION_STRING")