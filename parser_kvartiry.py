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

abain_bot = '1975239869:AAGytpbRIP0Gi8yO5_bj07MtyhTqmEPJc7I'
kvartirakgBot = '1904271012:AAH0GvWw_c1tlGv6o6tZe0sslZTQK3UZCEM'

bot = TeleBot(token=f'{kvartirakgBot}')
# Фильтрация обьявлений на от агентство и от частника
def filter_AN(link_user):
    r = requests.get(link_user, headers=headers, timeout=5)
    soup = Bs(r.text, features="html.parser")
    ads = (soup.findAll('a', class_='adTile-mainInfo'))

    n = 0
    for i in ads:
        i = i.get("href")

        if 'komnat' in str(i):
            n = n + 1

    print(n)
    if int(n) < 3:
        return None

    else:
        return True

# Добавление в базу новых обьявлений
def base_add(rooms, series, ploshad, remont, etaj, etaj_iz, rayon, prodaves, price, add_link, poslednyi_et, AN,
             photo_links,data_soz,data_prod):
    with sq.connect('version_1/lalago.db') as con:
        cur = con.cursor()

    cur.execute(
        f"INSERT INTO base (rooms,series,ploshad,remont,etaj,etaj_iz,rayon,prodaves, price, an, add_link, poslednyi_et, photo_links,data_soz, data_prod) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)",
        ( int(rooms), str(series), int(ploshad), str(remont), int(etaj), int(etaj_iz),str(rayon),str(prodaves), price, str(AN), str(add_link), str(poslednyi_et), str(photo_links) ,str(data_soz), str(data_prod)
        ))
    con.commit()

# Сравнение квартиры с похожимы квартирами
def osenka_kv(series, remont, rooms, rayon, etaj, etaj_iz, poslednyi_et):
    with sq.connect('../base_3.db') as con:
        cur = con.cursor()
    try:

        if int(etaj) == 1:
            info = (cur.execute(
                f"SELECT sum(ploshad), sum(price) FROM base WHERE rooms ='{rooms}' AND series = '{series}' AND remont = '{remont}' AND rayon = '{rayon}' AND price != '1'  GROUP BY rooms,series")).fetchone()
            price_srednyi = (int(info[1]) / int(info[0])) * 0.96

            return price_srednyi
        elif int(etaj) == int(etaj_iz):
            info = (cur.execute(
                f"SELECT sum(ploshad), sum(price) FROM base WHERE rooms ='{rooms}' AND series = '{series}' AND remont = '{remont}' AND rayon = '{rayon}' AND price != '1'  GROUP BY rooms,series")).fetchone()
            price_srednyi = (int(info[1]) / int(info[0])) * 0.96

            return price_srednyi
        else:
            info = (cur.execute(
                f"SELECT sum(ploshad), sum(price) FROM base WHERE rooms ='{rooms}' AND series = '{series}' AND remont = '{remont}' AND rayon = '{rayon}' AND price != '1'  GROUP BY rooms,series")).fetchone()
            price_srednyi = int(info[1]) / int(info[0])

            return price_srednyi

    except:
        pass




def Starter_check_lalafo_kg():
    while True:
        try:
            check_lalafo_kg()
            time.sleep(600)
        except:
            time.sleep(1800)
            continue

def check_lalafo_kg():
    rayon_list = {
        '3 мкр': ['3 мкр', '3мкр', '3мик', '3-ми', '3-мкр', '3 мик'],
        '4 мкр': ['4 мкр', '4мкр', '4мик', '4-ми', '4-мкр', '4 мик'],
        '5 мкр': ['5 мкр', '5мкр', '5мик', '5-ми', '5-мкр', '5 мик'],
        '6 мкр': ['6 мкр', '6мкр', '6мик', '6-ми', '6-мкр', '6 мик'],
        '7 мкр': ['7 мкр', '7мкр', '7мик', '7-ми', '7-мкр', '7 мик'],
        '8 мкр': ['8 мкр', '8мкр', '8мик', '8-ми', '8-мкр', '8 мик'],
        '9 мкр': ['9 мкр', '9мкр', '9мик', '9-ми', '9-мкр', '9 мик'],
        '10 мкр': ['10 мкр', '10мкр', '10мик', '10-ми', '10-мкр', '10 мик'],
        '11 мкр': ['11 мкр', '11мкр', '11мик', '11-ми', '11-мкр', '11 мик'],
        '12 мкр': ['12 мкр', '12мкр', '12мик', '12-ми', '12-мкр', '12 мик'],
        '110 квартал': ['110 квартал', '110-квартал'],
        '1000 мелочей (Карпинка)': ['карпин', '1000 мелоч', '1000-мелоч'],
        'Азамат авторынок': ['Азамат авторынок', 'Азамат авторынок', 'авторынок'],
        'Азия Молл': ['азия мол', 'азия-мол', 'Азия Молл'],
        'Ак-Бата ж/м': ['ак-бата', 'ак бата'],
        'Ак-Босого ж/м': ['ак-босого', 'ак босого'],
        'Ак-Жар ж/м': ['ак-жар', 'ак жар'],
        'Ак-Кеме (старый аэропорт)': ['ак-кеме', 'ак кеме', 'старый аэропорт',
                                      'старого аэропор', 'старый аеропорт',
                                      'старого аеропор'],
        'Ак-Орго ж/м': ['ак-орго', 'ак орго'],
        'Ак-Ордо 1 ж/м': ['ак-ордо 1', 'ак ордо 1', 'акордо 1'],
        'Ак-Ордо 2 ж/м': ['ак-ордо 1', 'ак ордо 2', 'акордо 2'],
        'Ак-Ордо 3 ж/м': ['ак-ордо 3', 'ак ордо 3', 'акордо 3'],
        'Ак-Ордо ж/м': ['ак-ордо', 'ак ордо', 'ак ордо', 'ак-ордо', 'акордо'],
        'Ак-Тилек ж/м': ['ак-тилек', 'актилек', 'ак тилек'],
        'Ала-Арча ТРЦ': ['ала-арча', 'ала арча'],
        'Ала-Арча ж/м': ['ала-арча ж/м', 'ж/м ала-арча', 'ж/м ала арча', 'ала арча ж/м'],
        'Ала-Тоо ж/м': ['Ала-Тоо ж/м', 'ив Ала-Тоо ж/м', 'Ала-Тоо ж/м'],
        'Аламедин-1 мкр': ['Аламедин 1', 'Аламедин-1', 'Аламедин1'],
        'Аламединский рынок / базар': ['Аламединс', 'рынок Аламедин', 'аламедин баз'],
        'Алтын-Казык ж/м': ['Алтын-Казык', 'Алтын Казык', 'Алтын-Казык ж/м',
                            'Алтын Казык ж/м', 'ж/м Алтын-Казык', 'ж/м Алтын Казык'],
        'Алтын-ордо ж/м': ['Алтын-ордо', 'Алтын ордо'],
        'Анар ж/м': ['Анар'],
        'Арча-Бешик ж/м': ['Арча-Бешик ж/м'],
        'Асанбай мкр': ['Асанбай', 'Асанбай мкр'],
        'Аска-Таш ж/м': ['Аска-Таш', 'Аска Таш'],
        'Ата-Журт ж/м': ['Ата-Журт ж/м', 'Ата-Журт ж/м'],
        'Ата-Тюрк парк': ['Ата-Тюрк', 'Ата Тюрк', 'Ата-турк', 'Ата турк', 'Ататюрк', 'Ататурк'],
        'Аэропорт Манас': ['Аэропорт Манас', 'Аэропорта Манас'],
        'БГУ': ['бгу', 'БГУ'],
        'Бакай-Ата ж/м': ['Бакай-Ата ж/м', 'Бакай-Ата'],
        'Баткенский рынок / базар': ['Баткенский рынок', 'рынок Баткен', 'баткен базар'],
        'Баят рынок / базар': ['Баят рынок / базар', 'Баят базар', 'рынок баят'],
        'Бета Сторес': ['Бета Сторес', 'Бета-Сторес'],
        'Бета Сторес 2': ['Бета Сторес 2', 'Бета-Сторес 2', 'Бета Сторес2', 'Бета-Сторес2'],
        'Биримдик-Кут ж/м': ['Биримдик-Кут', 'Биримдик Кут'],
        'Бишкек Парк ТРЦ': ['Бишкек Парк', 'Бишкек-Парк', 'БишкекПарк'],
        'Ботанический сад': [' Ботанический сад', 'Ботсад', 'Бот.сад'],
        'Бугу-Эне-Багыш ж/м': ['Бугу-Эне-Багыш', 'Бугу Эне Багыш'],
        'Бугу-Эне-Сай ж/м': [' Бугу-Эне-Сай', 'Бугу Эне Сай'],
        'Военный городок': [' Военный городок', 'Военный-городок'],
        'Восток-5 мкр': ['Восток-5', 'Восток 5', 'Восток5'],
        'Восточный (старый) автовокзал': [' Восточный автовокзал', ' Восточного автовокзал',
                                          'старый автовокзал', 'старого автовокзал',
                                          'Восточный(с', 'Восточный (с'],
        'Газ Городок': [' Газ Городок', ' Газ-Городок'],
        'Гоин': ['Гоин', 'гоин'],
        'Городок Энергетиков': [' Городок Энергетиков', ' Городок-Энергетиков'],
        'Городок строителей': [' Городок строителей', ' Городок-строителей'],
        'Городская больница №4 (ул. Айни)': ['айни', 'больница №4'],
        'Городское ГАИ': ['Городское ГАИ', 'гаи'],
        'Дворец спорта': ['Дворец спорта', 'Дворец-спорта'],
        'Джал мкр (в т.ч. Верхний, Нижний, Средний)': ['жал'],
        'Джунхай рынок': ['Джунхай рынок', 'Джунхай'],
        'Дордой-1 ж/м': ['Дордой-1 ж/м', 'Дордой-1'],
        'Дордой-2 ж/м': ['Дордой-2 ж/м', 'Дордой-2'],
        'Дордой Моторс рынок': ['Дордой Моторс', 'Дордой Моторс'],
        'Дордой рынок / базар': ['Дордой рынок', 'рынок дордой', 'дордой базар'],
        'Достук мкр': ['Достук', 'Достук мкр'],
        'ЖД вокзал': ['ЖД вокзал', 'ЖД-вокзал'],
        'Западный (новый) автовокзал': ['западного автовокзал', 'Западный автовокзал',
                                        'новый автовокзал'],
        'Интрегельпо': ['Интрегельпо', 'Интрегель'],
        'КНУ': ['кну', 'КНУ'],
        'Калыс-ордо ж/м': ['Калыс-ордо', 'Калыс-ордо ж/м'],
        'Кара-Жыгач ж/м': ['Кара-Жыгач', 'Кара Жыгач'],
        'Караван ТРЦ': ['Караван', 'Караван ТРЦ'],
        'Карагачевая роща': ['Карагачевая роща', 'Карагачевая-роща'],
        'Келечек ж/м': ['Келечек ж/м', 'ж/м Келечек'],
        'Керемет ж/м': ['Керемет ж/м', 'ж/м Керемет'],
        'Киргизия 1': ['Киргизия 1', 'Киргизия-1', 'Киргизия1', 'Киргизия'],
        'Киркомстром': ['Киркомстром', 'Кирком'],
        'Кирпичный Завод': ['Кирпичный Завод', 'Завод Кирпичный'],
        'Кожомкул стадион': ['Кожомкул стадион', 'стадион Кожомкул'],
        'Кок-Жар мкр': ['Кок Жар', 'Кок-Жар', 'кокжар'],
        'Колмо ж/м': ['Колмо ж/м', 'Колмо'],
        'Красный Строитель ж/м': ['Красный Строитель', 'Красный-Строитель'],
        'Кудайберген авторынок': ['Кудайберген', 'Кудайберген авторынок'],
        'Кызыл Аскер': ['Кызыл Аскер', 'Кызыл-Аскер'],
        'Кырман ж/м': ['Кырман ж/м', 'Кырман'],
        'Мадина рынок': ['Мадина', 'мадина'],
        'Мега Комфорт ТЦ': ['Мега Комфорт', 'Мега-Комфорт'],
        'Мед Академия': ['Мед Академия', 'МедАкадемия', 'Мед. Академия', 'Мед-Академия',
                         'Мед.Академия'],
        'Моссовет': ['Моссовет', 'Мосовет'],
        'Мурас-Ордо ж/м': ['Мурас-Ордо', 'Мурас Ордо'],
        'Орок ж/м': ['Орок', 'Орок ж/м'],
        'Ортосайский рынок / базар': ['Ортосай', 'Ортосайский рынок / базар'],
        'Оскон-ордо ж/м': ['Оскон-ордо', 'Оскон-ордо ж/м'],
        'Ошский рынок / базар': ['Ошский', 'ош базар'],
        'Панорама': ['Панорама', 'Панорама'],
        'Пишпек': ['Пишпек', 'Пишпек'],
        'Политех': ['Политех'],
        'Полицейский городок ж/м': ['Полицейский городок ж/м', 'Полицейский городок'],
        'Рабочий Городок': [' Рабочий Городок', ' Рабочий-Городок'],
        'Рухий Мурас ж/м': ['Рухий-Мурас', 'Рухий Мурас'],
        'Рынок Баят': ['Рынок Баят', 'Баят'],
        'Салам-Алик ж/м': ['Салам-Алик', 'Салам-Алик ж/м'],
        'Сары-Озон Дыйкан рынок': ['Сары-Озон', 'дыйкан', 'сары озон'],
        'Сары-Челек ж/м': ['Сары-Челек', 'Сары Челек'],
        'Совмина мкр': ['Совмина', 'Совмина мкр'],
        'Старый толчок рынок / базар': ['Старый толчок', 'Старый толчок рынок / базар'],
        'ТЭЦ': ['район ТЭЦ', 'районе ТЭЦ'],
        'Таатан ТЦ': ['Таатан', 'Таатан ТЦ'],
        'Таш-Добо ж/м': ['Таш-Добо', 'Таш Добо'],
        'Таш-Рабат ТРЦ': ['Таш-Рабат', 'Таш Рабат'],
        'Тендик ж/м': ['Тендик ж/м', 'Тендик'],
        'Токольдош': ['Токольдош', 'Токольдош'],
        'Тунгуч мкр': [' Тунгуч', 'Тунгуч '],
        'Тынчтык ж/м': ['Тынчтык ж/м', 'Тынчтык ж/м'],
        'Улан мкр': [' Улан', ' Улан мкр', 'Улан'],
        'Умут ж/м': [' Умут ж/м', ' Умут'],
        'Учкун мкр': [' Учкун', 'Учкун мкр'],
        'Физприборы': ['физприбор', 'физ.прибор', 'физ прибор'],
        'Филармония': [' Филармони', ' Филармония', 'Филармония '],
        'Центральная мечеть': ['Центральная мечеть', 'Центральный мечеть'],
        'Церковь': ['Церковь', 'Церков'],
        'Цум': ['Цум', 'Цум'],
        'Чекиш-Ата рынок': ['Чекиш-Ата рынок', 'Чекиш-Ата'],
        'Шлагбаум': ['район Шлагбаум', 'Шлагбаума'],
        'Шоро завод': ['Шоро завод', 'Шоро'],
        'Ынтымак ж/м': ['Ынтымак ж/м', ' Ынтымак ж'],
        'Эне-Сай ж/м': ['Эне-Сай', 'Эне-Сай ж/м'],
        'Энесай ж/м': ['Энесай', 'Энесай ж/м'],
        'Юг-2 мкр': ['Юг-2', 'Юг 2', 'Юг2'],
        'парк Фучика': ['Фучика', 'парк Фучика']}
    with sq.connect('version_1/lalago.db') as con:
        cur = con.cursor()
        add_link_list = cur.execute(f"SELECT link FROM link_kv").fetchall()
        for i in add_link_list:

            add_link = (((str(i)).replace("',)","")).replace("('","")).replace(' ','')
            print(add_link)

            with sq.connect('version_1/lalago.db') as con:
                cur = con.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS base (
                                                                           rooms INTEGER DEFAULT 0,
                                                                           series TEXT,
                                                                           ploshad INTEGER DEFAULT 0,
                                                                           remont TEXT,
                                                                           etaj INTEGER DEFAULT 0,
                                                                           etaj_iz INTEGER DEFAULT 0,
                                                                           rayon TEXT DEFAULT Бишкек,
                                                                           data_soz TEXT,
                                                                           data_prod TEXT,
                                                                           prodaves TEXT,
                                                                           price INTEGER DEFAULT 1,
                                                                           an TEXT,
                                                                           osenka TEXT,
                                                                           add_link TEXT,
                                                                           poslednyi_et TEXT,
                                                                           photo_links TEXT
                                                                           )""")
                # Проверка на уникальность обьявлений
                print('Проверка на уникальность...')
                cur.execute(f"SELECT add_link FROM base where add_link =?", (add_link,))
                try:
                    r = requests.get(add_link, headers=headers,proxies=get_proxy(proxy_list), timeout=5)
                    soup = Bs(r.text, features="html.parser")
                    data_info = soup.find_all('div', class_='about-ad-info__date')
                    print(data_info)
                except:
                    continue

                if str(data_info) == '[]':
                    print('не активно')
                else:
                    try:
                        if cur.fetchone() is None:

                            print('NEW ADS!!!')

                            # Парсим обявлений

                            price = soup.find('span', class_='heading international-price').text
                            print(price)
                            image = soup.find('div', class_='desktop css-10yjukn')

                            photo_links = []
                            for i in str(image).split('"'):

                                if 'https://img5.lalafo.com/i/posters/api' in i:
                                    i = i.replace("/api/", "/original/")

                                    if i in photo_links:
                                        continue
                                    else:
                                        photo_links.append(i)



                            try:
                                opisanie = soup.find('div', class_='description__wrap').text
                                link_user = 'https://lalafo.kg' + (soup.find('a', class_='userName')).attrs['href']
                            except:
                                print('ошибка получение ссылки пользователя или Описания!!!')

                            print('точка 1')

                            for i in data_info:
                                i = i.text
                                if 'Создано: ' in i:
                                    i = i.replace('Создано: ', '')
                                    data_soz = i
                                elif 'Обновлено: ' in i:
                                    i = i.replace('Обновлено: ', '')
                                    data_prod = i

                                else:
                                    data_soz = ' '
                                    data_prod = ' '
                                    continue

                            print('точка 2')

                            # Стандартизация цены
                            price = price.replace('USD', '').replace(' ', '').replace('KGS', '')
                            parameters = soup.find('ul', class_='details-page__params css-tl517w')
                            remont = ' '
                            series = ' '
                            ploshad = '0'
                            etaj = '0'
                            etaj_iz = '0'
                            rayon = ' '
                            prodaves = ' '
                            rooms = '0'
                            poslednyi_et = ' '

                            print('точка 3')

                            try:
                                print('parametr', parameters)
                                for i in parameters:
                                    if 'Площадь (м2):' in i.text:
                                        i = i.text
                                        i = i.replace('Площадь (м2):', '')
                                        ploshad = i

                                    elif 'Количество комнат:' in i.text:
                                        i = i.text
                                        i = i.replace('Количество комнат:', '').replace(' комнаты', '').replace(
                                            ' комната',
                                            '').replace(' комнат', '')

                                        rooms = i
                                        if rooms == 'Студия':
                                            rooms = 1


                                    elif 'Этаж:' in i.text:
                                        i = i.text
                                        i = i.replace('Этаж:', '')
                                        etaj = i

                                    elif 'Количество этажей:' in i.text:
                                        i = i.text
                                        i = i.replace('Количество этажей:', '')
                                        etaj_iz = i

                                    elif 'Район:' in i.text:
                                        i = i.text
                                        i = i.replace('Район:', '')
                                        rayon = i


                                    elif 'Тип предложения:' in i.text:
                                        i = i.text
                                        i = i.replace('Тип предложения:', '')
                                        prodaves = i

                                    elif 'Серия:' in i.text:
                                        i = i.text
                                        i = i.replace('Серия:', '')
                                        series = i

                                    elif 'Ремонт:' in i.text:
                                        i = i.text
                                        i = i.replace('Ремонт:', '')
                                        remont = i

                                    else:
                                        continue

                                # Анализ текста для опеределения данных

                                if series == ' ':

                                    elitka_list = ['элитка', 'элитный', 'премиум', 'элит']
                                    seria_102 = ['102 серия', '102 сер', '102сер', '102']
                                    seria_104 = ['104 серия', '104 сери', '104сер', '104']
                                    seria_105 = ['105 серия', '105 сери', '105сер', '105']
                                    seria_106 = ['106 серия', '106 сери', '106сер', '106']
                                    hrishevka = ['хрущёвка', 'хрущевка', 'хруш', "хрущ"]

                                    for i in seria_102:
                                        if i in opisanie:
                                            series = "102 серия"
                                        else:
                                            continue

                                    for i in seria_104:
                                        if i in opisanie:
                                            series = '104 серия'
                                        else:
                                            continue

                                    for i in seria_105:
                                        if i in opisanie:
                                            series = '105 серия'
                                        else:
                                            continue

                                    for i in seria_106:
                                        if i in opisanie:
                                            series = '106 серия'
                                        else:
                                            continue

                                    for i in hrishevka:
                                        if i in opisanie:
                                            series = 'Хрущёвка'
                                        else:
                                            continue

                                    for i in elitka_list:
                                        if i in opisanie:
                                            series = 'Элитка'
                                        else:
                                            continue

                                print('Стандартизация ремонта')
                                if remont == ' ':

                                    bez_remont = ['псо', 'без ремонта', 'требуеться рем', 'ПСО', 'самоотделк',
                                                  'само отде', 'под само']
                                    st_remont = ['старый ремонт', 'ремонт старый', "требуеться косм", 'состояние сре']
                                    sv_remont = ['свежий ремонт', 'новый ремонт', 'ремонт', 'обои', 'состояние']
                                    ev_remont = ['Евроремонт', 'евро', 'Eвроремонт', 'техника', 'мебел']

                                    for i in st_remont:
                                        if i in opisanie:
                                            remont = 'Старый ремонт'
                                        else:
                                            continue

                                    for i in sv_remont:
                                        if i in opisanie:
                                            remont = 'Свежий ремонт'
                                        else:
                                            continue

                                    for i in bez_remont:
                                        if i in opisanie:
                                            remont = 'Без ремонта'

                                        else:
                                            continue
                                    for i in ev_remont:
                                        if i in opisanie:
                                            remont = 'Евроремонт'

                                        else:
                                            continue

                                print('Стандартизация Района')

                                if rayon == ' ':

                                    for k, v in rayon_list.items():
                                        for i in v:
                                            if i in opisanie:
                                                rayon = k

                                print('Стандартизация площади')
                                # Стандартизация площади
                                series = str(series)
                                rooms = int(rooms)

                                if series == '102 серия':

                                    if rooms == 1:
                                        ploshad = 30

                                    elif rooms == 2:
                                        ploshad = 42

                                    elif rooms == 3:
                                        ploshad = 56


                                elif series == "104 серия":

                                    if rooms == 1:
                                        ploshad = 32

                                    elif rooms == 2:
                                        ploshad = 43

                                    elif rooms == 3:
                                        ploshad = 58


                                elif series == "104 серия улучшенная":

                                    if rooms == 1:
                                        ploshad = 30

                                    elif rooms == 2:
                                        ploshad = 42

                                    elif rooms == 3:
                                        ploshad = 56
                                elif series == "105 серия":

                                    if rooms == 1:
                                        ploshad = 34

                                    elif rooms == 2:
                                        ploshad = 50

                                    elif rooms == 3:
                                        ploshad = 62

                                    elif rooms == 4:
                                        ploshad = 74

                                    elif rooms == 5:
                                        ploshad = 87


                                elif series == "105 серия улучшенная":
                                    if rooms == 1:
                                        ploshad = 34

                                    elif rooms == 2:
                                        ploshad = 50

                                    elif rooms == 3:
                                        ploshad = 62

                                    elif rooms == 4:
                                        ploshad = 74

                                    elif rooms == 5:
                                        ploshad = 87


                                elif series == "106 серия":
                                    if rooms == 1:
                                        ploshad = 35


                                    elif rooms == 2:
                                        ploshad = 52

                                    elif rooms == 3:
                                        ploshad = 66


                                elif series == "106 серия улучшенная":
                                    if rooms == 1:
                                        ploshad = 35

                                    elif rooms == 2:
                                        ploshad = 52

                                    elif rooms == 3:
                                        ploshad = 66


                                elif series == "Хрущёвка":
                                    if rooms == 1:
                                        ploshad = 30

                                    elif rooms == 2:
                                        ploshad = 42

                                    elif rooms == 3:
                                        ploshad = 56

                                else:
                                    pass


                            except:
                                print('Точка 4')

                            print('Точка 5')

                            AN = str(filter_AN(link_user=link_user))

                            print('точка 7')

                            if price == 'Договорная':
                                continue

                            try:
                                # Проверка на выгодность квартиры

                                if 5 < int(ploshad) < 350:
                                    if 280 < int(price) < 1800:
                                        price = int(ploshad) * int(price)

                                    if int(etaj) == int(etaj_iz):
                                        poslednyi_et = 'последний этаж'


                                    # Оценка на выгодность

                                    sr_price = osenka_kv(series=series, remont=remont, rooms=rooms, rayon=rayon,
                                                         etaj=etaj,
                                                         etaj_iz=etaj_iz, poslednyi_et=poslednyi_et)

                                    price_m2 = round(int(price) / int(ploshad))
                                    sr_price = int(sr_price)

                                    if int(price_m2) < int(sr_price):
                                        print('Оценка: TRUE')
                                        osenka = 'Выгодный'
                                        if rayon == ' ':
                                            print('Район пустой')
                                            continue

                                    else:

                                        osenka = 'Выше среднего'

                                    base_add(rooms=rooms, series=series, ploshad=ploshad, remont=remont, etaj=etaj,
                                             etaj_iz=etaj_iz, rayon=rayon, prodaves=prodaves, price=price, AN=AN,
                                             add_link=add_link, poslednyi_et=poslednyi_et, photo_links=photo_links,
                                             data_soz=data_soz, data_prod=data_prod)

                                    print('Добавлено в базу!!!')


                                else:
                                    print('Не корректный площад')
                                    base_add(rooms=rooms, series=series, ploshad=ploshad, remont=remont, etaj=etaj,
                                             etaj_iz=etaj_iz, rayon=rayon, prodaves=prodaves, price=price, AN=AN,
                                             add_link=add_link, poslednyi_et=poslednyi_et, photo_links=photo_links, data_soz=data_soz,data_prod=data_prod)

                                    print('Добавлено в базу!!!')
                                    continue

                            except:

                                base_add(rooms=rooms, series=series, ploshad=ploshad, remont=remont, etaj=etaj,
                                         etaj_iz=etaj_iz, rayon=rayon, prodaves=prodaves, price=price, AN=AN,
                                         add_link=add_link, poslednyi_et=poslednyi_et, photo_links=photo_links,
                                         data_soz=data_soz, data_prod=data_prod)

                                print('exept')






                            print('Обновление базы!!!')
                            print(osenka)

                            with sq.connect('version_1/lalago.db') as con:
                                cur = con.cursor()

                                cur.execute("""CREATE TABLE IF NOT EXISTS base (
                                                                                                       rooms INTEGER DEFAULT 0,
                                                                                                       series TEXT,
                                                                                                       ploshad INTEGER DEFAULT 0,
                                                                                                       remont TEXT,
                                                                                                       etaj INTEGER DEFAULT 0,
                                                                                                       etaj_iz INTEGER DEFAULT 0,
                                                                                                       rayon TEXT DEFAULT Бишкек,
                                                                                                       data_soz TEXT,
                                                                                                       data_prod TEXT,
                                                                                                       prodaves TEXT,
                                                                                                       price INTEGER DEFAULT 1,
                                                                                                       an TEXT,
                                                                                                       osenka TEXT,
                                                                                                       add_link TEXT,
                                                                                                       poslednyi_et TEXT,
                                                                                                       photo_links TEXT
                                                                                                       )""")

                                cur.execute(
                                    f"UPDATE base SET osenka = '{str(osenka)}' WHERE add_link = '{str(add_link)}' ")

                                con.commit()
                            print('ОЦЕНКА ОБНОВЛЕНО!!!')

                        else:
                            pass



                    except:
                        continue


Thread(target=Starter_check_lalafo_kg(), args=()).start()






