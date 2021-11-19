from notenews import Functions, filter_owner
from client import Config, NoteNews

from pyrogram.types import Message
from pyrogram import filters

import heroku3

from functools import partial, wraps
import time


cmd = partial(filters.command, prefixes=list("/"))

#
import feedparser
@NoteNews.on_message(cmd("kek"))
async def kek(_, message: Message):
    feed = feedparser.parse("https://www.gizmochina.com/feed")
    entry = feed.entries[0]
    link = entry.link
    title = entry.title
    await message.reply(f"{title}\n\n{link}")
#
@NoteNews.on_message(cmd("add") & filter_owner)
async def add_feed(_, message: Message):
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
    if not Functions.input_str(message) == "-yt":
        for url in Config.FEED_URLS:
            msg += f"{url}\n"
        await message.reply(msg, quote=True)
        return
    for url in Config.YT_URLS:
        msg += f"{url}\n"
    await message.reply(url, quote=True)
