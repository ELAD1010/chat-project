import os
from server.decorators.singleton import singleton

@singleton
class AppConfig:
    def __init__(self):
        self.ip = os.getenv('IP')
        self.port = int(os.getenv('PORT'))
        self.db_name = os.getenv('DB_NAME')