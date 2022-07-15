# -*- coding: utf-8 -*-
import sqlite3 as sq
import time
import requests
from bs4 import BeautifulSoup as Bs
from telebot import TeleBot
from telebot import types
from threading import Thread
from fake_useragent import UserAgent
from PIL import Image
import imagehash
import distance
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
bot = TeleBot(token=f'{botapi}')

def Starter_botmen():
    while True:
        try:
            botmen()
            time.sleep(10)
        except:
            time.sleep(10)
            continue


def botmen():
    global hash_import_photo
    hash_import_photo = []
    @bot.message_handler(commands=['start'])
    def start_command(message):
        bot.send_message(message.chat.id, text='Отправьте ссылку на обьявления или фото квартиры для поиска дубликатов!!!')


    @bot.message_handler(content_types=['text'])
    def get_text_message(message):
        if '----' in message.text:
            i = (str(message.text)).split("----")
            parser_hash_hamming(user=message.chat.id, link=i[0], dist=i[1])

        elif 'bishkek/ads/' in message.text:
            parser_hash(user=message.chat.id, link=message.text)


        elif message.text == 'Найти квартиру по фото':

            bot.send_message(message.chat.id, text=f'Поиск по фото начать ....', reply_markup=types.ReplyKeyboardRemove())

            parser_hash_photo(user=message.chat.id, hash_photos=hash_import_photo)




        else:
            parser_hash(user=message.chat.id, link=message.text)
            bot.send_message(message.chat.id, text='Не настроенная комманда!!!')



    @bot.message_handler(content_types=['photo'])

    def photo(message):
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        photo_link = f'https://api.telegram.org/file/bot{kvartirakgBot}/{file_info.file_path}'
        image_data = Image.open(requests.get(photo_link, stream=True).raw)
        hash = imagehash.phash(image_data)
        hash_import_photo.append(str(hash))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Найти квартиру по фото')
        markup.add(btn1)
        bot.send_message(message.chat.id, text='фото получень',reply_markup=markup)



    bot.polling(none_stop=True)
def parser_hash_hamming(user, link, dist):

    with sq.connect('version_1/lalago.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT add_link FROM db_hash_images where add_link =?", (link,))

    if cur.fetchone() is None:

        r = requests.get(link, headers=headers,timeout=5)
        soup = Bs(r.text, features="html.parser")
        image = soup.find('div', class_='desktop css-10yjukn')
        images_hash = []
        unique = []
        for i in str(image).split('"'):
            unique = []
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

        finder_hash = []
        for i in images_hash:
            if i in finder_hash:
                continue
            else:
                finder_hash.append(i)



        cur.execute(
            f'INSERT INTO db_hash_images (add_link,images_hash) VALUES("{link}", "{finder_hash}")')
        con.commit()

        with sq.connect('version_1/lalago.db') as con:
            cur = con.cursor()
            base_image_hash = cur.execute("""SELECT add_link, images_hash FROM db_hash_images""").fetchall()

        result = []

        for i in finder_hash:
            for a, b in base_image_hash:
                for c in b.split(","):
                    c = (((c.replace("'", "")).replace("[", '')).replace("]", "")).replace(' ', '')
                    try:
                        r = distance.hamming(str(i), str(c))
                        if r < dist:
                            if a in result:
                                pass
                            else:
                                result.append(a)
                        else:
                            continue
                    except:
                        continue


    else:

        with sq.connect('version_1/lalago.db') as con:
            cur = con.cursor()
        image_hash = cur.execute(f"SELECT images_hash FROM db_hash_images WHERE add_link = '{link}'").fetchone()
        list = ((((str(image_hash)).replace('("[', '')).replace(']",)','')).replace("'", "")).replace(' ','')
        finder_hash = []
        for i in list.split(","):
            if i in finder_hash:
                continue
            else:
                finder_hash.append(i)

        base_image_hash = cur.execute("""SELECT add_link, images_hash FROM db_hash_images""").fetchall()


        result = []

        for i in finder_hash:
            for a, b in base_image_hash:
                for c in b.split(","):
                    c = (((c.replace("'", "")).replace("[", '')).replace("]", "")).replace(' ', '')
                    try:
                        r = distance.hamming(str(i), str(c))
                        if int(r) < int(dist):
                            if a in result:
                                pass
                            else:
                                result.append(a)
                        else:
                            continue
                    except:
                        continue

        for b in result:

            price = ''
            data_soz = ''
            data_prod = ''
            link_user = ''
            try:
                r = requests.get(b, headers=headers)
                soup = Bs(r.text, features="html.parser")
                data_info = soup.find_all('div', class_='about-ad-info__date')
                price = soup.find('span', class_='heading').text
                link_user = 'https://lalafo.kg' + (soup.find('a', class_='userName')).attrs['href']

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
                # Стандартизация цены
                price = price.replace('USD', '').replace(' ', '').replace('KGS', '')
                bot.send_message(user,
                                 text=f'Цена: {price}\nДата создания: {data_soz}\nДата продления: {data_prod}\n{b}\n\nАвтор: {link_user}')

            except:
                bot.send_message(user,
                                 text=f'Цена: {price}\nДата создания: {data_soz}\nДата продления: {data_prod}\n{b}\n\nАвтор: {link_user}')

                continue
def parser_hash(user,link):
    with sq.connect('version_1/lalago.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT add_link FROM db_hash_images where add_link =?", (link,))
    if cur.fetchone() is None:

        r = requests.get(link, headers=headers,timeout=5)
        soup = Bs(r.text, features="html.parser")

        if 'bishkek/ads' in link:
            image = soup.find('div', class_='desktop css-10yjukn')
            images_hash = []
            unique = []
            for i in str(image).split('"'):
                unique = []
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

            finder_hash = []
            for i in images_hash:
                if i in finder_hash:
                    continue
                else:
                    finder_hash.append(i)

            cur.execute(
                f'INSERT INTO db_hash_images (add_link,images_hash) VALUES("{link}", "{finder_hash}")')
            con.commit()

        elif 'stroka' in link:

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

            finder_hash = []
            for i in images_hash2:
                if i in finder_hash:
                    continue
                else:
                    finder_hash.append(i)

            cur.execute(
                f'INSERT INTO db_hash_images (add_link,images_hash) VALUES("{link}", "{finder_hash}")')
            con.commit()

        elif 'house.kg' in link:
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
            finder_hash = []
            for i in images_hash3:
                if i in finder_hash:
                    continue
                else:
                    finder_hash.append(i)

            cur.execute(
                f'INSERT INTO db_hash_images (add_link,images_hash) VALUES("{link}", "{finder_hash}")')
            con.commit()




        else:

            bot.send_message(user, text='Не известная команда!!!')




        with sq.connect('base_image.db') as con:
            cur = con.cursor()
            base_image_hash = cur.execute("""SELECT add_link, images_hash FROM db_hash_images""").fetchall()

        result = []

        for a in finder_hash:
            for b, c in base_image_hash:
                if a in c:
                    if b in result:
                        pass
                    else:
                        result.append(b)

                    list = ((((str(c)).replace("[", '')).replace("]", '')).replace("'", "")).replace(' ', '')
                    finder_hash2 = []

                    for i in list.split(","):
                        if i in finder_hash2:
                            pass
                        else:
                            finder_hash2.append(i)

                    for d in finder_hash2:
                        for f, g in base_image_hash:
                            if d in g:
                                if f in result:
                                    pass
                                else:

                                    result.append(f)

                            else:
                                continue


                else:
                    continue

        for b in result:
            price = ''
            data_soz = ''
            data_prod = ''
            link_user = ''

            if 'bishkek/ads' in b:
                try:
                    r = requests.get(b, headers=headers)
                    soup = Bs(r.text, features="html.parser")
                    data_info = soup.find_all('div', class_='about-ad-info__date')
                    price = soup.find('span', class_='heading').text
                    link_user = 'https://lalafo.kg' + (soup.find('a', class_='userName')).attrs['href']

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
                    # Стандартизация цены
                    price = price.replace('USD', '').replace(' ', '').replace('KGS', '')
                    bot.send_message(user,
                                     text=f'Цена: {price}\nДата создания: {data_soz}\nДата продления: {data_prod}\n{b}\n\nАвтор: {link_user}')
                except:

                    continue

            elif 'stroka' in b:
                try:
                    r = requests.get(b, headers=headers)
                    soup = Bs(r.text, features="html.parser")
                    price = soup.find('span', class_='topic-view-best-rows-value')
                    data_prod = soup.find('div',
                                          class_='topic-view-date_list-item topic-view-topic_date_up ic_date_range_9c9c9c_24dp_2x')
                    data_soz = soup.find('div', class_='topic-view-date_list-item topic-view-topic_date_create_row')
                    price = price.text
                    data_soz = data_soz.text
                    data_prod = data_prod.text
                    bot.send_message(user,
                                     text=f'Цена: {price}\n{data_soz}\n{data_prod}\n{b}\n')
                except:
                    continue


            elif 'house.kg' in b:
                try:
                    r = requests.get(b, headers=headers)
                    soup = Bs(r.text, features="html5lib")
                    data_soz = soup.find('span', class_='added-span')
                    data_prod = soup.find('span', class_='upped-span')
                    price = soup.find('div', class_='price-dollar')
                    price = ((price.text).replace('$', '')).replace(' ', '')
                    bot.send_message(user,
                                     text=f'Цена: {price}\n{data_soz.text}\n{data_prod.text}\n{b}\n')

                except:
                    continue

            else:
                continue





    else:
        with sq.connect('version_1/lalago.db') as con:
            cur = con.cursor()
        image_hash = cur.execute(f"SELECT images_hash FROM db_hash_images WHERE add_link = '{link}'").fetchone()
        list = ((((str(image_hash)).replace('("[', '')).replace(']",)','')).replace("'", "")).replace(' ','')
        finder_hash = []
        for i in list.split(","):
            if i in finder_hash:
                continue
            else:
                finder_hash.append(i)

        base_image_hash = cur.execute("""SELECT add_link, images_hash FROM db_hash_images""").fetchall()


        result = []

        for a in finder_hash:
            for b, c in base_image_hash:
                if a in c:
                    if b in result:
                        pass
                    else:
                        result.append(b)

                    list = ((((str(c)).replace("[", '')).replace("]", '')).replace("'", "")).replace(' ','')
                    finder_hash2 = []
                    for i in list.split(","):
                        if i in finder_hash2:
                            pass
                        else:
                            finder_hash2.append(i)

                    for d in finder_hash2:
                        for f, g in base_image_hash:
                            if d in g:
                                if f in result:
                                    pass
                                else:

                                    result.append(f)

                            else:
                                continue


                else:
                    continue

        for b in result:
            price = ''
            data_soz = ''
            data_prod = ''
            link_user = ''

            if 'bishkek/ads' in b:
                try:
                    r = requests.get(b, headers=headers)
                    soup = Bs(r.text, features="html.parser")
                    data_info = soup.find_all('div', class_='about-ad-info__date')
                    price = soup.find('span', class_='heading').text
                    link_user = 'https://lalafo.kg' + (soup.find('a', class_='userName')).attrs['href']

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
                    # Стандартизация цены
                    price = price.replace('USD', '').replace(' ', '').replace('KGS', '')
                    bot.send_message(user,
                                     text=f'Цена: {price}\nДата создания: {data_soz}\nДата продления: {data_prod}\n{b}\n\nАвтор: {link_user}')
                except:

                    continue

            elif 'stroka' in b:
                try:
                    r = requests.get(b, headers=headers)
                    soup = Bs(r.text, features="html.parser")
                    price = soup.find('span', class_='topic-view-best-rows-value')
                    data_prod = soup.find('div',
                                          class_='topic-view-date_list-item topic-view-topic_date_up ic_date_range_9c9c9c_24dp_2x')
                    data_soz = soup.find('div', class_='topic-view-date_list-item topic-view-topic_date_create_row')
                    price = price.text
                    data_soz = data_soz.text
                    data_prod = data_prod.text
                    bot.send_message(user,
                                     text=f'Цена: {price}\n{data_soz}\n{data_prod}\n{b}\n')
                except:
                    continue


            elif 'house.kg' in b:
                try:
                    r = requests.get(b, headers=headers)
                    soup = Bs(r.text, features="html5lib")
                    data_soz = soup.find('span', class_='added-span')
                    data_prod = soup.find('span', class_='upped-span')
                    price = soup.find('div', class_='price-dollar')
                    price = ((price.text).replace('$','')).replace(' ','')
                    bot.send_message(user,
                                     text=f'Цена: {price}\n{data_soz.text}\n{data_prod.text}\n{b}\n')

                except:
                    continue

            else:
                continue
def parser_hash_photo(user, hash_photos):

    with sq.connect('version_1/lalago.db') as con:
        cur = con.cursor()
    base_image_hash = cur.execute("""SELECT add_link, images_hash FROM db_hash_images""").fetchall()

    result = []

    finder_hash = []
    for i in hash_photos:
        if i in finder_hash:
            continue
        else:
            finder_hash.append(i)
    global hash_import_photo
    hash_import_photo = []



    for a in finder_hash:
        for b, c in base_image_hash:
            if a in c:
                if b in result:
                    pass
                else:
                    result.append(b)

                list = ((((str(c)).replace("[", '')).replace("]", '')).replace("'", "")).replace(' ', '')
                finder_hash2 = []
                for i in list.split(","):
                    if i in finder_hash2:
                        pass
                    else:
                        finder_hash2.append(i)

                for d in finder_hash2:
                    for f, g in base_image_hash:
                        if d in g:
                            if f in result:
                                pass
                            else:

                                result.append(f)

                        else:
                            continue


            else:
                continue


    if str(result) == '[]':
        bot.send_message(user, text='Не найдено!!!')

    for b in result:
        price = ''
        data_soz = ''
        data_prod = ''
        link_user = ''

        if 'bishkek/ads' in b:
            try:
                r = requests.get(b, headers=headers)
                soup = Bs(r.text, features="html.parser")
                data_info = soup.find_all('div', class_='about-ad-info__date')
                price = soup.find('span', class_='heading').text
                link_user = 'https://lalafo.kg' + (soup.find('a', class_='userName')).attrs['href']

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
                # Стандартизация цены
                price = price.replace('USD', '').replace(' ', '').replace('KGS', '')
                bot.send_message(user,
                                 text=f'Цена: {price}\nДата создания: {data_soz}\nДата продления: {data_prod}\n{b}\n\nАвтор: {link_user}')
            except:

                continue

        elif 'stroka' in b:
            try:
                r = requests.get(b, headers=headers)
                soup = Bs(r.text, features="html.parser")
                price = soup.find('span', class_='topic-view-best-rows-value')
                data_prod = soup.find('div',
                                      class_='topic-view-date_list-item topic-view-topic_date_up ic_date_range_9c9c9c_24dp_2x')
                data_soz = soup.find('div', class_='topic-view-date_list-item topic-view-topic_date_create_row')
                price = price.text
                data_soz = data_soz.text
                data_prod = data_prod.text
                bot.send_message(user,
                                 text=f'Цена: {price}\n{data_soz}\n{data_prod}\n{b}\n')
            except:
                continue


        elif 'house.kg' in b:
            try:
                r = requests.get(b, headers=headers)
                soup = Bs(r.text, features="html5lib")
                data_soz = soup.find('span', class_='added-span')
                data_prod = soup.find('span', class_='upped-span')
                price = soup.find('div', class_='price-dollar')
                price = ((price.text).replace('$', '')).replace(' ', '')
                bot.send_message(user,
                                 text=f'Цена: {price}\n{data_soz.text}\n{data_prod.text}\n{b}\n')

            except:
                continue

        else:
            continue


Thread(target=Starter_botmen, args=()).start()