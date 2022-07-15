import psycopg2
from config import host, user, password, db_name

try:
    print(host)
    con = psycopg2.connect(host=host,user=user,password = password,db_name=db_name)
    with con.cursor() as cursor:
        cursor.execute("SELECT version();")
        print(cursor.fetchone())
except:
    pass