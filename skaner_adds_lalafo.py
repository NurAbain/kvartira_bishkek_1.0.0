# -*- coding: utf-8 -*-
from telebot import types
import sqlite3 as sq
from datetime import date
import time
import datetime
import requests
from bs4 import BeautifulSoup as Bs
from telebot import TeleBot
from fake_useragent import UserAgent
import random
from threading import Thread
from config import *

def get_proxy(proxy_list):
    proxy = random.choice(proxy_list)
    proxies = {"http": f'http://{proxy}', "https": f'http://{proxy}'}
    return proxies
def get_useragent():
    my_browser = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    try:
        ua = UserAgent(fallback=my_browser)
        my_agent = ua.random

        return my_agent

    except Exception as e:
        print(e)
        return my_browser

headers = {'User-Agent': get_useragent()}


def Starter_skaner_kvartir_lalafo():
    while True:
        try:
            skaner_kvartir_lalafo()
            time.sleep(600)
        except:
            time.sleep(1800)
            continue

def skaner_kvartir_lalafo():
    for i in range(0, 1200):
        try:
            with sq.connect('lalago.db') as con:
                cur = con.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS link_kv (
                link TEXT,
                scan_date TEXT
                )""")

            print(f'СТРАНИЦА: {i}')
            url = f'https://lalafo.kg/bishkek/kvartiry/prodazha-kvartir?page={i}'
            r = requests.get(url, headers=headers,proxies=get_proxy(proxy_list), timeout=5)
            soup = Bs(r.text, features="html.parser")
            scan_date = datetime.date.today()
            print(scan_date)
            for i in str(soup).split('"'):
                if '/bishkek/ads/' in i:
                    add_link = 'https://lalafo.kg' + i
                    cur.execute(f"SELECT link FROM link_kv where link =?", (add_link,))
                    try:
                        if cur.fetchone() is None:

                            cur.execute(
                                f"INSERT INTO link_kv (link, scan_date) VALUES(?, ?)",
                                (
                                    str(add_link), str(scan_date)))
                            con.commit()
                        else:

                            continue
                    except:
                        continue
            time.sleep(5)
        except:
            time.sleep(600)


def start():
    Thread(target=Starter_skaner_kvartir_lalafo(), args=()).start()

start()


