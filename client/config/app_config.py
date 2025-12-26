import os


class AppConfig:
    def __init__(self):
        self.ip = os.getenv('IP')
        self.port = int(os.getenv('PORT'))