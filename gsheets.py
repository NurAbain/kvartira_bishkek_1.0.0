# Подключаем библиотеки
import httplib2
import googleapiclient.discovery
import sqlite3 as sq
from datetime import date
import time
from oauth2client.service_account import ServiceAccountCredentials
from threading import Thread

CREDENTIALS_FILE = '../bishkek-kvartira-052fdf7db38e.json'


#Имя файла с закрытым ключом, вы должны подставить свое
# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API
#
# spreadsheet = service.spreadsheets().create(body = {
#     'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'},
#     'sheets': [{'properties': {'sheetType': 'GRID',
#                                'sheetId': 0,
#                                'title': 'Лист номер один',
#                                'gridProperties': {'rowCount': 1000, 'columnCount': 15}}}]
# }).execute()
spreadsheetId = '1xUGGawlhL6ywU0kOjU-1QowEJyFcwYaWdhl95I9mBzA' # сохраняем идентификатор файла


print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)

driveService = googleapiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API


# access = driveService.permissions().create(
#     fileId = spreadsheetId,
#     body = {'type': 'user', 'role': 'writer', 'emailAddress': 'nurlanmilliarder@gmail.com'},  # Открываем доступ на редактирование
#     fields = 'id'
# ).execute()

# # Добавление листа
# results = service.spreadsheets().batchUpdate(
#     spreadsheetId=spreadsheetId,
#     body=
#     {
#         "requests": [
#             {
#                 "addSheet": {
#                     "properties": {
#                         "title": "Бишкек",
#                         "gridProperties": {
#                             "rowCount": 20,
#                             "columnCount": 12
#                         }
#                     }
#                 }
#             }
#         ]
#     }).execute()

# Получаем список листов, их Id и название

spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
sheetList = spreadsheet.get('sheets')
for sheet in sheetList:
    print(sheet['properties']['sheetId'], sheet['properties']['title'])
sheetId = sheetList[0]['properties']['sheetId']
print('Мы будем использовать лист с Id = ', sheetId)
def photos(photo_links):
    if len(photo_links) < 5:
        return photo_links
    return photo_links[:5:]



#Парсер lalafo.kg
def Starter_gsheets():
    while True:
        try:
            gsheets()
            time.sleep(1800)
            print('SLEEP-30')
        except:
            print('EXEPT')
            time.sleep(200)
            continue
def gsheets():

    with sq.connect('../base_3.db') as con:
        cur = con.cursor()
    result = cur.execute(f"SELECT price, rooms, ploshad, series,remont,etaj, etaj_iz, rayon, add_link, photo_links  FROM base WHERE an = 'None' AND osenka='Выгодный' ").fetchall()
    zapros_ob_1 = []
    zapros_ob_2 = []
    zapros_ob_3 = []
    zapros_ob_4 = []

    for price, rooms, ploshad, series,remont,etaj, etaj_iz, rayon,add_link, photo_links in result:
        photo_links = photos(photo_links.split(','))
        zapros = [f'{price}',f'{round(int(price)/int(ploshad))}', f'{rooms}', f'{ploshad}', series,remont,f'{etaj}', f'{etaj_iz}', rayon]
        for i in photo_links:
            i = (((i.replace("[","")).replace("'","")).replace("]","")).replace(" ","")
            zapros.append(i)
        if rooms == 1:
            zapros_ob_1.append(zapros)
        elif rooms == 2:
            zapros_ob_2.append(zapros)
        elif rooms == 3:
            zapros_ob_3.append(zapros)
        else:
            zapros_ob_4.append(zapros)


    request = service.spreadsheets().values().clear(spreadsheetId=spreadsheetId, range='1-к!A2:N3000')
    response = request.execute()
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED", "data": [ {"range": "1-к!A2:N3000", "majorDimension": "ROWS", "values": zapros_ob_1}]}).execute()

    request = service.spreadsheets().values().clear(spreadsheetId=spreadsheetId, range='2-к!A2:N3000')
    response = request.execute()
    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": "2-к!A2:N3000", "majorDimension": "ROWS", "values": zapros_ob_2}]}).execute()

    request = service.spreadsheets().values().clear(spreadsheetId=spreadsheetId, range='3-к!A2:N3000')
    response = request.execute()
    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": "3-к!A2:N3000", "majorDimension": "ROWS", "values": zapros_ob_3}]}).execute()

    request = service.spreadsheets().values().clear(spreadsheetId=spreadsheetId, range='4-к!A2:N3000')
    response = request.execute()
    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": "4-к!A2:N3000", "majorDimension": "ROWS", "values": zapros_ob_4}]}).execute()







Thread(target=Starter_gsheets, args=()).start()


# results = service.spreadsheets().batchUpdate(spreadsheetId = spreadsheetId, body = {
#   "requests": [
#
#     # Задать ширину столбца A: 20 пикселей
#     {
#       "updateDimensionProperties": {
#         "range": {
#           "sheetId": sheetId,
#           "dimension": "COLUMNS",  # Задаем ширину колонки
#           "startIndex": 0, # Нумерация начинается с нуля
#           "endIndex": 1 # Со столбца номер startIndex по endIndex - 1 (endIndex не входит!)
#         },
#         "properties": {
#           "pixelSize": 20 # Ширина в пикселях
#         },
#         "fields": "pixelSize" # Указываем, что нужно использовать параметр pixelSize
#       }
#     },
#
#     # Задать ширину столбцов B и C: 150 пикселей
#     {
#       "updateDimensionProperties": {
#         "range": {
#           "sheetId": sheetId,
#           "dimension": "COLUMNS",
#           "startIndex": 1,
#           "endIndex": 3
#         },
#         "properties": {
#           "pixelSize": 150
#         },
#         "fields": "pixelSize"
#       }
#     },
#
#     # Задать ширину столбца D: 200 пикселей
#     {
#       "updateDimensionProperties": {
#         "range": {
#           "sheetId": sheetId,
#           "dimension": "COLUMNS",
#           "startIndex": 6,
#           "endIndex": 7
#         },
#         "properties": {
#           "pixelSize": 250
#         },
#         "fields": "pixelSize"
#       }
#     }
#   ]
# }).execute()