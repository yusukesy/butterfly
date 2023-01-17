import os


from bs4 import BeautifulSoup as bs
import requests

from time import sleep
import random

from .sql import db
from apscheduler.schedulers.background import BackgroundScheduler

from pyrogram.errors import FloodWait
from client import Config, NoteNews
	
	
def get_file_url(link):
	html = requests.get(link).content
	soup = bs(html, "html.parser")
	file = soup.find("div", "list-group").find_all("a")
	for i in file:
	    if "imperatriz" in i["href"]:
	        file_url = i["href"]
	title = file_url.split("/")[9]
	return file_url, title

def down_file(file_url, path):
	content = requests.get(file_url).content
	try:
		with open(path, "wb") as file:
			file.write(content)
		NoteNews.send_document("-1001165341477", path)
	except Exception as e:
	    NoteNews.send_message("-1001165341477", str(e))
	    print(str(e))
	else:
	    print("OK!")
		
		
def check_send():
    #website = "https://www.adorocinema.com/noticias-materias-especiais/"
    website = "https://estudenoifma.ifma.edu.br/"
    html = requests.get(website).content
    soup = bs(html, "html.parser")
    # author = "Adoro Cinema" #
    #title = str(soup.main.h2.a.string)
    #link = "https://www.adorocinema.com" + str(soup.main.h2.a.get("href"))
    link = str(soup.main.h3.a["href"])
    if link is not None:
        if db.get_link(website) == None:
            db.update_link(website, "*")
            return
        if link != db.get_link(website).link:
            message = f"Essa porra já saiu, olha aí: {link}"
            #message = f"""
#[\u200c]({link})🌐 | via **Adoro Cinema:** **[{title}]({link})**
#
#▫️ | Mantido por: @NoteZV
#"""
            try:
                #NoteNews.send_message(Config.LOG_CHANNEL, message)
                NoteNews.send_message("-1001165341477" , message)
                
                file_url, title = get_file_url(link)
                down_file(file_url, title)
                sleep(10)
                os.remove(title)
                
                db.update_link(website, link)
            except FloodWait as e:
                print(f"FloodWait: {e.x} segundos")
                sleep(e.x)
            except Exception as e:
                print(str(e))
        else:
            NoteNews.send_message("-1001165341477", f"FEED verificado: {link}")#print(f"FEED Verificado: {link}")
            
scheduler = BackgroundScheduler()
scheduler.add_job(check_send, "interval", seconds=Config.CHECK_INTERVAL, max_instances=Config.MAX_INSTANCES)
scheduler.start()
