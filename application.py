from sqlalchemy import create_engine
import mysql.connector
from dotenv import load_dotenv
import os
import json
import pandas as pd
from flask import Flask, request, render_template
load_dotenv()

application = Flask(__name__)

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

engine = create_engine(f'mysql+mysqldb://{db_user}:{db_passwd}@{db_host}:{db_port}/{db_name}')
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/ids")
def get_ids():
    query = "SELECT distinct driver_id FROM Driving_Record_A"
    ids = pd.read_sql(query, engine)
    return ids.to_json(orient='records')


@app.route("/api/records/<driver_id>")
def get_records(driver_id):
    query = f"SELECT * FROM Driving_Record_A WHERE driver_id = '{driver_id}' ORDER BY date, hour"
    records = pd.read_sql(query, engine)
    records['Hour'] = records['Hour'].apply(lambda x: f"{str(x).zfill(2)}:00")
    #adding (s) to the end of the data to make it more readable
    records['TotalOfOverSpeedTime'] = records['TotalOfOverSpeedTime'].apply(lambda x: f"{x}(s)")
    records['TotalNeturalSlideTime'] = records['TotalNeturalSlideTime'].apply(lambda x: f"{x}(s)")
    
    return records.to_json(orient='records')
    

@app.route("/api/records/<driver_id>/<date>")
def get_records_with_date(driver_id, date):
    query = f"SELECT * FROM Driving_Record_A WHERE driver_id = '{driver_id}' AND date = '{date}' ORDER BY date, hour"
    records = pd.read_sql(query, engine)
    records['Hour'] = records['Hour'].apply(lambda x: f"{str(x).zfill(2)}:00")
    #adding (s) to the end of the data to make it more readable
    records['TotalOfOverSpeedTime'] = records['TotalOfOverSpeedTime'].apply(lambda x: f"{x}(s)")
    records['TotalNeturalSlideTime'] = records['TotalNeturalSlideTime'].apply(lambda x: f"{x}(s)")
    
    return records.to_json(orient='records')

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