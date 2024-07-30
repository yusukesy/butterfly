import os
import importlib

from whatsapp_api_client_python import API

class Config:
    API_ID = "7103963554"
    API_TOKEN = "571383a58c5248df8fd83788a2e235167c3f1a0caf564bde82"
    NUMBER = "99992004698@c.us"
    # FEED_URLS = list(set(i for i in os.environ.get("FEED_URLS").split(" | ")))
    # YT_URLS = list(set(i for i in os.environ.get("YT_URLS").split(" | ")))
    # LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL"))
    CHECK_INTERVAL = 10
    MAX_INSTANCES = 10

NoteNews = API.GreenAPI(Config.API_ID, Config.API_TOKEN)