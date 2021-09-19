import os
# import random
from time import sleep, time

import feedparser
from .sql import db
from apscheduler.schedulers.background import BackgroundScheduler

from pyrogram.errors import FloodWait
from client import Config, NoteNews


def check_send():
    feeds_url = ["http://feeds.feedburner.com/youtube/einerd/feed", "http://feeds.feedburner.com/DevAprender"]
    for feed_url in feeds_url:
        feed_url = feed_url
    # feed_url = random.choice(Config.FEED_URLS)
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
        try:
            NoteNews.send_photo(-1001165341477, entry.media_thumbanil[0]["url"], message)
            db.update_link(feed_url, entry.id)
        except FloodWait as e:
            print(f"FloodWait: {e.x} segundos")
            sleep(e.x)
        except Exception as e:
            print(e)
    else:
        print(f"FEED Verificado: {entry.id}")

scheduler = BackgroundScheduler()
scheduler.add_job(check_send, "interval", seconds=Config.CHECK_INTERVAL, max_instances=Config.MAX_INSTANCES)
scheduler.start()
