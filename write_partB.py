import time
import mysql.connector
from dotenv import load_dotenv
import os
import random
load_dotenv()

driver_id = ["duxu1000009","hanhui1000002","haowei1000008","likun1000003","panxian1000005","shenxian1000004","xiexiao1000001","zengpeng1000000","zouan1000007"]
car_plate_number = ["华AT75H8","华AZI419","华A709GB","华AVM936","华AX542C","华ADJ750","华AEB132","华AZQ110","华A58M83"]
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

def genData():
    driver = random.randint(0,8)

    speed=20 + random.randint(1,70)
    Time = int(time.time())
    data = {}
    data['driver'] = driver_id[driver]
    data['car'] = car_plate_number[driver]
    data['time'] = Time
    data['speed'] = speed
    data['overspeed'] = True if speed > 60 else False
    return data

def execute():
    data = genData()
    sql = "insert into Driving_Record_B(driver_id, CarPlateNumber, ctime, Speed, Overspeed) values ('%s', '%s', %d, %d, %d)" % (data['driver'], data['car'], data['time'], data['speed'], data['overspeed'])
    print(sql)
    ret = cur.execute(sql)

while True:
    execute()
    time.sleep(10)