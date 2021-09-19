import os
import random
from time import sleep, time

import feedparser
from .sql import db
from apscheduler.schedulers.background import BackgroundScheduler

from pyrogram.errors import FloodWait
from client import Config, NoteNews

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def check_sends():
    feed_url = random.choice(Config.YT_URLS)
    FEED = feedparser.parse(feed_url)
    entry = FEED.entries[0]
    if db.get_link(feed_url) == None:
        db.update_link(feed_url, "*")
        return
    if entry.id != db.get_link(feed_url).link:
        message = f"""
🌐 via {entry.author} | @NoteZV
╰• {entry.title}
"""
        buttons = [[InlineKeyboardButton(text="Assistir ao vídeo", url=entry.link)]]
        try:
            NoteNews.send_photo(-1001165341477, entry.media_thumbnail[0]["url"], caption=message, reply_markup=InlineKeyboardMarkup(buttons))
            db.update_link(feed_url, entry.id)
        except FloodWait as e:
            print(f"FloodWait: {e.x} segundos")
            sleep(e.x)
        except Exception as e:
            print(e)
    else:
        print(f"FEED Verificado: {entry.id}")

schedulera = BackgroundScheduler()
schedulera.add_job(check_sends, "interval", seconds=5, max_instances=Config.MAX_INSTANCES)
schedulera.start()