import os

class Config:
    def __init__(self):
        self.ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "")
        self.ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
        self.MITM_PORT = 8082
        self.STORAGE_FILE = os.getenv("STORAGE_FILE", "/root/tg-mitm-system/data.json")

config = Config()
