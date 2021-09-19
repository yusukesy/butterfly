import os
import random
from time import sleep, time

import feedparser
from .sql import db
from apscheduler.schedulers.background import BackgroundScheduler

from pyrogram.errors import FloodWait
from client import Config, NoteNews


def check_sends():
    feeds_url = ["http://feeds.feedburner.com/youtube/einerd/feed", "http://feeds.feedburner.com/DevAprender"]
    feed_url = random.choice(feeds_url)
    print("HEREEEEEE: " + feed_url)
    FEED = feedparser.parse(feed_url)
    entry = FEED.entries[0]
    print(entry)
    if db.get_link(feed_url) == None:
        db.update_link(feed_url, "*")
        return
    if entry.id != db.get_link(feed_url).link:
        message = f"""
🌐 via {entry.author} | @NoteZV
╰• {entry.title}
"""
        try:
            NoteNews.send_message(-1001165341477, message)
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