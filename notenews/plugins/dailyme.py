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
    urls = "https://www.tecmundo.com.br/tecnologia/"
    website = urls
    html = requests.get(urls).content
    soup = bs(html, "html.parser")
    author = "TecMundo"
    title = str(soup.find("div", attrs={"class": "tec--list__item"}).div.a.string)
    link = str(soup.find("div", attrs={"class": "tec--list__item"}).div.a.get("href"))
    if link is not None:
        if db.get_link(website) == None:
            db.update_link(website, "*")
            return
        if link != db.get_link(website).link:
            message = f"""
[\u200c]({link})🌐 | via **Adoro Cinema:** **[{title}]({link})**

▫️ | Mantido por: @NoteZV
"""
            try:
                NoteNews.send_message(-1001165341477, message)
                db.update_link(website, link)
            except FloodWait as e:
                print(f"FloodWait: {e.x} segundos")
                sleep(e.x)
            except Exception as e:
                print(str(e))
            else:
                print(f"FEED Verificado: {link}")
                
scheduler = BackgroundScheduler()
scheduler.add_job(check_send, "interval", seconds=1, max_instances=Config.MAX_INSTANCES)
scheduler.start()
