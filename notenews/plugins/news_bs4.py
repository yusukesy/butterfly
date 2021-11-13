from bs4 import BeautifulSoup as bs
import requests

from time import sleep
import random

from .sql import db
from apscheduler.schedulers.background import BackgroundScheduler

from pyrogram.errors import FloodWait
from client import Config, NoteNews


def check_send():
    website_  = ["https://www.adorocinema.com/noticias-materias-especiais/", "https://www.omelete.com.br/noticias"]
    website = random.choice(website_)
    html = requests.get(website).content
    soup = bs(html, "html.parser")
    # author = "Adoro Cinema" #
    title = str(soup.main.h2.a.string) if website != "https://www.omelete.com.br/noticias" else str(soup.main.a.h2.string)
    link = "https://www.adorocinema.com" + str(soup.main.h2.a.get("href")) if website != "https://www.omelete.com.br/noticias" else "https://www.omelete.com.br" + str(soup.main.a.get("href"))
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
scheduler.add_job(check_send, "interval", seconds=Config.CHECK_INTERVAL, max_instances=Config.MAX_INSTANCES)
scheduler.start()
