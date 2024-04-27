import mysql.connector
from dotenv import load_dotenv
import os
import json
import pandas as pd
from flask import Flask, request, render_template
load_dotenv()

application = Flask(__name__)

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_passwd = os.getenv('DB_PASSWD')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')

def db_connection():
    mydb = mysql.connector.connect( host = db_host,
    user = db_user ,
    port = db_port,
    database = db_name,
    passwd = db_passwd,
    autocommit = True)
    return mydb

mydb = db_connection()
cur = mydb.cursor()

@application.route("/")
def index():
    return render_template("index.html")

@application.route("/api/ids")
def get_ids():
    sql = "SELECT distinct driver_id FROM Driving_Record_A"
    cur.execute(sql)
    ids = cur.fetchall()
    df = pd.DataFrame(ids)
    df.columns = ['driver_id']    
    return df.to_json(orient='records')


@application.route("/api/records/<driver_id>")
def get_records(driver_id):
    query = f"SELECT * FROM Driving_Record_A WHERE driver_id = '{driver_id}' ORDER BY date, hour"
    cur.execute(query)
    records = cur.fetchall()
    records = pd.DataFrame(records)
    records[4] = records[4].apply(lambda x: f"{str(x).zfill(2)}:00")
    #adding (s) to the end of the data to make it more readable
    records[5] = records[5].apply(lambda x: f"{x}(s)")
    records[7] = records[7].apply(lambda x: f"{x}(s)")
    
    df = pd.DataFrame(records)
    return df.to_json(orient='records')
    

@application.route("/api/records/<driver_id>/<date>")
def get_records_with_date(driver_id, date):
    query = f"SELECT * FROM Driving_Record_A WHERE driver_id = '{driver_id}' AND date = '{date}' ORDER BY date, hour"
    cur.execute(query)
    records = cur.fetchall()
    records = pd.DataFrame(records)
    records[4] = records[4].apply(lambda x: f"{str(x).zfill(2)}:00")
    #adding (s) to the end of the data to make it more readable
    records[5] = records[5].apply(lambda x: f"{x}(s)")
    records[7] = records[7].apply(lambda x: f"{x}(s)")

    df = pd.DataFrame(records)

    return df.to_json(orient='records')

@application.route("/liveView")
def liveView():
    return render_template("liveView.html")

tmp_time = 0

@application.route('/liveData')
def getData():
    global tmp_time
    driver_id = request.args.get('driver_id')
    if tmp_time > 0 :
        sql = "select * from Driving_Record_B where driver_id = '%s' AND  ctime >%s order by ctime desc" %(driver_id, tmp_time)
    else:
        sql = "select * from Driving_Record_B where driver_id = '%s' order by ctime desc" %(driver_id)
    
    cur.execute(sql)
    datas = []
    for i in cur.fetchall():
        datas.append([i[0], i[1], i[2], i[3], i[4], i[5]])
    
    if len(datas) > 0 :
        tmp_time = datas[-1][0]
    
    return json.dumps(datas)
    
@application.route('/drivers')
def get_drivers():
    sql = "SELECT DISTINCT driver_id FROM Driving_Record_B"
    cur.execute(sql)
    drivers = cur.fetchall()
    print ("drivers: ", drivers)
    return json.dumps(drivers)

if __name__ == "__main__":
	application.run(port=5000)