# -*- coding: utf-8 -*-
import sqlite3 as sq
import time
import requests
from bs4 import BeautifulSoup as Bs
from threading import Thread
from fake_useragent import UserAgent
from PIL import Image
import imagehash
import random
from config import *


def get_proxy(proxy_list):
    proxy = random.choice(proxy_list)
    proxies = {"http": f'http://{proxy}', "https": f'http://{proxy}'}
    return proxies


def get_useragent():
    my_browser = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17/Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    try:
        ua = UserAgent(fallback=my_browser,verify_ssl=False)
        my_agent = ua.random

        return my_agent

    except Exception as e:
        print(e)
        return my_browser

headers = {'User-Agent': get_useragent()}

def Starter_parser_stroka():
    while True:
        try:
            check_stroka_kg()
            time.sleep(30)
        except:

            time.sleep(20)
            continue
def Starter_parser_house_kg():
    while True:
        try:

            chech_house_kg()
            time.sleep(30)
        except:

            time.sleep(20)
            continue
def Starter_parser_lalafo():
    while True:
        try:

            check_lalafo_kg()
            time.sleep(30)

        except:

            time.sleep(60)
            continue

def check_lalafo_kg():

    with sq.connect('version_1/lalago.db') as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS db_hash_images (add_link TEXT, images_hash TEXT)""")
        con.commit()
        list_link = cur.execute(f"SELECT link FROM link_kv ")
        colvo = 0
        for add_link in list_link:
            try:
                add_link = ((str(add_link)).replace("',)",'')).replace("('","")
                print(add_link)
                cur = con.cursor()
                cur.execute(f"SELECT add_link FROM db_hash_images where add_link =?", (add_link,))

                if cur.fetchone() is None:
                    colvo = colvo + 1

                    # Парсим обявлений
                    r = requests.get(add_link, headers=headers, proxies=get_proxy(proxy_list), timeout=5)
                    soup = Bs(r.text, features="html.parser")
                    image = soup.find('div', class_='desktop css-10yjukn')

                    images_hash = []
                    unique = []
                    for i in str(image).split('"'):

                        if 'https://img5.lalafo.com/i/posters/api' in i:
                            if i in unique:
                                continue
                            else:
                                unique.append(i)
                                try:
                                    image_data = Image.open(requests.get(i, stream=True).raw)

                                    hash = imagehash.phash(image_data)

                                    images_hash.append(str(hash))
                                except:
                                    continue


                    if str(images_hash) == '[]':

                        for i in str(image).split('"'):
                            if 'https://img5.lalafo.com/i/posters/' in i:
                                if i in unique:
                                    continue
                                else:
                                    unique.append(i)
                                    try:
                                        image_data = Image.open(requests.get(i, stream=True).raw)

                                        hash = imagehash.phash(image_data)

                                        images_hash.append(str(hash))
                                    except:
                                        continue

                    if str(images_hash) == '[]':
                        continue

                    else:
                        print(add_link)
                        print(images_hash)
                        cur = con.cursor()
                        cur.execute(f'INSERT INTO db_hash_images (add_link,images_hash) VALUES(?,?)',(str(add_link),str(images_hash)))
                        con.commit()
                        continue

                else:
                    print('уже в базе!!!')
                    continue

            except Exception as e:
                print('exept1')
                print(e)
                continue

        print('connect')
def check_stroka_kg():
    for i in range(0, 15):
        #ФИЛЬТР ПОСЛЕДНИЕ СОЗДАННЫЕ
        url = f'https://stroka.kg/kupit-kvartiru/?q=&topic_image=on&order=date&cost_min=&cost_max=&topic_point=bishkek&p={i}#paginator'
        # url = 'https://stroka.kg/kupit-kvartiru/?q&order=date&cost_min&cost_max&topic_point=bishkek'
        r = requests.get(url, headers=headers, proxies=get_proxy(proxy_list), timeout=5)
        soup = Bs(r.text, features="html.parser")
        list = soup.find_all('a', class_='topics-item-view')

        for i in list:
            i = i['href']
            add_link = i.replace('amp;', '')  # Ссылка на обьявления
            with sq.connect('version_1/lalago.db') as con:
                cur = con.cursor()

                cur.execute(f"SELECT add_link FROM db_hash_images where add_link =?", (add_link,))

                if cur.fetchone() is None:

                    r = requests.get(add_link, headers=headers)
                    soup = Bs(r.text, features="html.parser")
                    image_url = soup.find_all('div', class_='topic-best-view-block-50 topic-best-view-block-50__image')

                    images_hash2 = []
                    unique2 = []
                    for i in (str(image_url)).split("'"):
                        if 'https://data.stroka.kg/image' in i:

                            if i in unique2:
                                continue
                            else:
                                unique2.append(i)
                                try:

                                    image_data = Image.open(requests.get(i, stream=True).raw)
                                    hash = imagehash.phash(image_data)
                                    images_hash2.append(str(hash))

                                except:
                                    continue

                    if str(images_hash2) == '[]':
                        continue
                    else:
                        cur.execute(
                            f'INSERT INTO db_hash_images (add_link,images_hash) VALUES("{add_link}", "{images_hash2}")')
                        con.commit()


                else:

                    continue
def chech_house_kg():
    for i in range(1, 1000):

        try:
            url = f'https://www.house.kg/kupit-kvartiru?region=1&town=2&has_photo=1&sort_by=m2_price+asc&page={i}'
            r = requests.get(url, headers=headers, timeout=5)
            soup = Bs(r.text, features="html.parser")
            link = soup.find_all('p', class_='title', )
            for i in link:
                try:
                    add_link_house = 'https://www.house.kg' + str(i.find('a').get('href'))
                    with sq.connect('version_1/lalago.db') as con:
                        cur = con.cursor()
                        cur.execute(f"SELECT add_link FROM db_hash_images where add_link =?", (add_link_house,))

                    if cur.fetchone() is None:
                        r = requests.get(add_link_house, headers=headers, timeout=5)
                        soup = Bs(r.text, features="html.parser")
                        images_hash3 = []
                        unique = []
                        for i in (str(soup)).split('"'):
                            if '1200x900.jpg' in i:
                                if i in unique:
                                    continue
                                else:
                                    unique.append(i)
                                    try:
                                        image_data = Image.open(requests.get(i, stream=True).raw)
                                        hash = imagehash.phash(image_data)
                                        images_hash3.append(str(hash))
                                    except:
                                        continue

                        if str(images_hash3) == '[]':
                            continue
                        else:
                            cur.execute(
                                f'INSERT INTO db_hash_images (add_link,images_hash) VALUES("{add_link_house}", "{images_hash3}")')
                            con.commit()

                    else:
                        continue

                except:
                    print('ОШИБКА ВНУТРИ ОБЬЯВЛЕНИИ HAUSE.KG')
                    continue

        except:
            print('Ошибка на странице!!!')
            continue



def start():
    Thread(target=Starter_parser_lalafo, args=()).start()
    Thread(target=Starter_parser_stroka, args=()).start()
    Thread(target=Starter_parser_house_kg, args=()).start()

