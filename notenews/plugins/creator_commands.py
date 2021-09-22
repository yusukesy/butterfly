from notenews import Functions
from client import Config, NoteNews

from pyrogram.types import Message
from pyrogram import filters

import heroku3

from functools import partial, wraps
import time

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
        
@NoteNews.on_message(cmd("del"))
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
        
        
@NoteNews.on_message(cmd("idk"))
async def idk(_, message: Message):
    if Functions.check_owner(message.from_user.id) == True:
        if not Functions.input_str(message) == "-yt":
            await message.reply(Config.FEED_URLS, quote=True)
            return
        await message.reply(Config.YT_URLS, quote=True)
        
        
        
        
        
import schedule, time

def enviar():
    NoteNews.send_message(-1001165341477, "@NoteZV\n\nPELO AMOR SE DEUS, FAÇA O QUE O PROFESSOR DE MATEMÁTICA PEDIU. VEJA O QUE ELE DISSE NO GRUPO DA ESCOLA, PLMDS.\n@NoteZV")
    

schedule.every().day.at("15:30").do(enviar)

while 1:
    schedule.run_pending()
    time.sleep(1)