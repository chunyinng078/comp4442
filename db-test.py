import mysql.connector
from dotenv import load_dotenv
import os
import json
load_dotenv()


def db_connection():
    mydb = mysql.connector.connect( host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    port = os.getenv('DB_PORT'),
    database = os.getenv('DB_NAME'),
    passwd = os.getenv('DB_PASSWD'),
    autocommit = True)
    return mydb

mydb = db_connection()
cur = mydb.cursor()


# print db
sql = "SELECT * FROM Driving_Record_B"
cur.execute(sql)
datas = []
for i in cur.fetchall():
    datas.append(i[0], i[1], i[2], i[3], i[4], i[5])
print (datas)
