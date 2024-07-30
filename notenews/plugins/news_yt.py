import os
import random
from time import sleep, time

import feedparser
from .sql import db
from apscheduler.schedulers.background import BackgroundScheduler

from client import Config, NoteNews


def check_send():
    feed_url = random.choice(Config.YT_URLS)
    FEED = feedparser.parse(feed_url)
    entry = FEED.entries[0]
    if db.get_link(feed_url) == None:
        db.update_link(feed_url, "*")
        return
    if entry.id != db.get_link(feed_url).link:
        message = f"{entry.link}"
        try:
            NoteNews.sending.sendMessage(Config.NUMBER, message)
        except FloodWait as e:
            print(f"FloodWait: {e.x} segundos")
            sleep(e.x)
        except Exception as e:
            print(e)
    else:
        print(f"YT Verificado: {entry.id}")

scheduler = BackgroundScheduler()
scheduler.add_job(check_send, "interval", seconds=Config.CHECK_INTERVAL, max_instances=Config.MAX_INSTANCES)
scheduler.start()