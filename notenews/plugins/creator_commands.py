from notenews import Functions
from client import Config, NoteNews

from pyrogram.types import Message
from pyrogram import filters

import heroku3

from functools import partial, wraps
import time

cmd = partial(filters.command, prefixes=list("/"))

CREATOR_ID = 1157759484

async def check_owner(_, __, message: Message) -> bool:
    if message.from_user.id == CREATOR_ID:
        return True
    return False
    
filter_owner = filters.create(check_owner)


@NoteNews.on_message(cmd("add") & filter_owner)
async def add_feed(_, message: Message):
    if Functions.check_owner(message.from_user.id) == True:
        heroku_conn = heroku3.from_key(Config.HU_KEY)
        app = heroku_conn.apps()[Config.HU_APP]
        heroku_vars = app.config()
        url = Functions.input_str(message)
        if not url[:3] == "-yt":
            var = heroku_vars["FEED_URLS"]
            msg: Message = await message.reply("`Feed adicionado ✅\nReiniciando...`", quote=True)
            time.sleep(3)
            await msg.delete(); await message.delete()
            heroku_vars["FEED_URLS"] = f"{var} | {url}"
            return
        var = heroku_vars["YT_URLS"]
        mns: Message = await message.reply("`Canal adicionado ✅\nReiniciando...`", quote=True)
        time.sleep(3)
        await mns.delete(); await message.delete()
        heroku_vars["YT_URLS"] = f"{var} | {url[4:]}"
        
@NoteNews.on_message(cmd("del") & filter_owner)
async def del_feed(_, message: Message):
    if Functions.check_owner(message.from_user.id) == True:
        heroku_conn = heroku3.from_key(Config.HU_KEY)
        app = heroku_conn.apps()[Config.HU_APP]
        heroku_vars = app.config()
        url = Functions.input_str(message)
        if not url[:3] == "-yt":
            var = heroku_vars["FEED_URLS"]
            msg: Message = await message.reply("`Feed removido ❎\nReiniciando...`", quote=True)
            time.sleep(3)
            await msg.delete(); await message.delete()
            heroku_vars["FEED_URLS"] = var.replace(f" | {url}", "")
            return
        var = heroku_vars["YT_URLS"]
        mns: Message = await message.reply("`Canal removido ❎\nReiniciando...`", quote=True)
        time.sleep(3)
        await mns.delete(); await message.delete()
        heroku_vars["YT_URLS"] = var.replace(f" | {url[4:]}", "")
        
        
@NoteNews.on_message(cmd("idk") & filter_owner)
async def idk(_, message: Message):
    msg = ""
    if Functions.check_owner(message.from_user.id) == True:
        if not Functions.input_str(message) == "-yt":
            for url in Config.FEED_URLS:
                msg += f"{url}\n"
            await message.reply(msg, quote=True)
            return
        for url in Config.YT_URLS:
            msg += f"{url}\n"
        await message.reply(url, quote=True)
