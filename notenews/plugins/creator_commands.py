from notenews import Functions
from client import Config, NoteNews

from pyrogram.types import Message
from pyrogram import filters

import heroku3


from functools import partial, wraps

cmd = partial(filters.command, prefixes=list("/"))


@NoteNews.on_message(cmd("add"))
async def add_feed(_, message: Message):
    if Functions.check_owner(message.from_user.id) == True:
        heroku_conn = heroku3.from_key(Config.HU_KEY)
        app = heroku_conn.apps()[Config.HU_APP]
        heroku_vars = app.config()
        url = Functions.input_str(message)
        if not url[:3] == "-yt":
            var = heroku_vars["FEED_URLS"]
            await message.reply("Feed adicionado! Reiniciando...", quote=True)
            heroku_vars["FEED_URLS"] = f"{var} | {url}"
            return
        var = heroku_vars["YT_URLS"]
        await message.reply("Canal adicionado! Reiniciando...", quote=True)
        heroku_vars["YT_URLS"] = f"{var} | {url[4:]}"
        
@NoteNews.on_message(cmd("del"))
async def del_feed(_, message: Message):
    if Functions.check_owner(message.from_user.id) == True:
        heroku_conn = heroku3.from_key(Config.HU_KEY)
        app = heroku_conn.apps()[Config.HU_APP]
        heroku_vars = app.config()
        url = Functions.input_str(message)
        if not url[:3] == "-yt":
            var = heroku_vars["FEED_URLS"]
            await message.reply("Feed removido! Reiniciando...", quote=True)
            heroku_vars["FEED_URLS"] = var.replace(f" | {url}", "")
            return
        var = heroku_vars["YT_URLS"]
        await message.reply("Canal removido! Reiniciando...", quote=True)
        heroku_vars["YT_URLS"] = var.replace(f" | {url[4:]}", "")
        
        
@NoteNews.on_message(cmd("idk"))
async def idk(_, message: Message):
    if Functions.check_owner(message.from_user.id) == True:
        heroku_conn = heroku3.from_key(Config.HU_KEY)
        app = heroku_conn.apps()[Config.HU_APP]
        heroku_vars = app.config()["FEED_URLS"].split(" | ")
        
