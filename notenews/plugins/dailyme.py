from bs4 import BeautifulSoup as bs
import feedparser
import requests

from time import sleep
import random

from .sql import db
from apscheduler.schedulers.background import BackgroundScheduler

from pyrogram.errors import FloodWait
from client import Config, NoteNews


def check_send():
    websites = ["http://feeds.feedburner.com/gizmocn", "http://feeds.feedburner.com/feedburner/canaltech", "https://www.tecmundo.com.br/tecnologia/"]
    website = random.choice(websites)
    html = requests.get(website).content
    soup = bs(html, "html.parser")
    if website == "https://www.tecmundo.com.br/tecnologia/":
        author = "TecMundo"
        title = str(soup.find("div", attrs={"class": "tec--list__item"}).div.a.string)
        link = str(soup.find("div", attrs={"class": "tec--list__item"}).div.a.get("href"))
    if website == "http://feeds.feedburner.com/feedburner/canaltech":
        author = "CanalTech"
        feed = feedparser.parse(website)
        entry = feed.entries[0]
        title = entry.title
        link_ = entry.link
        if not (link_.startswith("https://canatech.com.br/smartphone") or link_.startswith("https://canatech.com.br/tecnologia") or link_.startswith("https://canatech.com.br/tablet") or link_.startswith("https://canatech.com.br/windows") or link_.startswith("https://canatech.com.br/fone-de-ouvido") or link_.startswith("https://canatech.com.br/casa-conectada") or link_.startswith("https://canatech.com.br/internet") or link_.startswith("https://canatech.com.br/notebook") or link_.startswith("https://canatech.com.br/software")):
            link = None
            return
        link = link_
    if website == "http://feeds.feedburner.com/gizmocn":
        author = "GizmoChina"
        feed = feedparser.parse(website)
        entry = feed.entries[0]
        link = entry.link
        title = entry.title
    if link is not None:
        if db.get_link(website) == None:
            db.update_link(website, "*")
            return
        if link != db.get_link(website).link:
            message = f"""
[\u200c]({link})🌐 | via **{author}:** **[{title}]({link})**

▫️ | Mantido por: @NoteZV
"""
            try:
                NoteNews.send_message(-1001666072628, message)
                db.update_link(website, link)
            except FloodWait as e:
                print(f"FloodWait: {e.x} segundos")
                sleep(e.x)
            except Exception as e:
                print(str(e))
        else:
            print(f"FEED Verificado: {link}")
            
scheduler = BackgroundScheduler()
scheduler.add_job(check_send, "interval", seconds=100, max_instances=Config.MAX_INSTANCES)
scheduler.start()
