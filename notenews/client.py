import os

from pyrogram import Client


class Config:
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = str(os.environ.get("API_HASH"))
    BOT_TOKEN = str(os.environ.get("BOT_TOKEN"))
    HU_KEY = str(os.environ.get("HU_KEY"))
    HU_APP = str(os.environ.get("HU_APP"))
    
    FEED_URLS = list(set(i for i in os.environ.get("FEED_URLS").split(" | ")))
    # YT_URLS = list(set(i for i in os.environ.get("YT_URLS").split(" | ")))
    LOG_CHANNEL = str(os.environ.get("LOG_CHANNEL"))
    CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL"))
    MAX_INSTANCES = int(os.environ.get("MAX_INSTANCES"))

class NoteBot(Client):
    def __init__(self):
        kwargs = {
            'api_id': Config.API_ID,
            'api_hash': Config.API_HASH,
            'session_name': ":memory:",
            'bot_token': Config.BOT_TOKEN
        }
        super().__init__(**kwargs)

    async def start(self):
        await super().start()
        print("START")
        try:
            for p in os.listdir("notenews/plugins"):
                if p.endswith(".py"):
                    arq = p.replace(".py", "")
                    importlib.import_module("plugins." + arq)
        except Exception as e:
            print(str(e))
            await self.send_message(-100116534147, f"**❌ OCORREU UM ERRO**\n\nNão foi possível importar os plugins, ocorreu este erro: `{str(e)}`")
        else:
            await self.send_message(-1001165341477, "`NoteNews iniciado com sucesso!`")

    async def stop(self):
        await super().stop()
        print("STOP")
    
NoteNews = NoteBot()
