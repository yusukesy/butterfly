from bs4 import BeautifulSoup as bs
import requests

from time import sleep
import random

from .sql import db
from apscheduler.schedulers.background import BackgroundScheduler

from pyrogram.errors import FloodWait
from client import Config, NoteNews


def check_send():
    urls = ["https://www.omelete.com.br/noticias", "https://www.adorocinema.com/noticias-materias-especiais/"]
    website = random.choice(urls)
    html = requests.get(website).content
    soup = bs(html, "html.parser")
    author = "Omelete" if website == "https://www.omelete.com.br/noticias" else "Adoro Cinema"
    title = str(soup.main.a.h2.string) if website == "https://www.omelete.com.br/noticias" else str(soup.main.h2.a.string)
    link = "https://omelete.com.br" + str(soup.main.a.get("href")) if website == "https://www.omelete.com.br/noticias" else "https://www.adorocinema.com" + str(soup.main.h2.a.get("href"))
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
                NoteNews.send_message(Config.LOG_CHANNEL, message)
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
