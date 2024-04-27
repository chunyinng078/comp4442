import flask
import mysql.connector
from dotenv import load_dotenv
import os
import json
from flask import Flask, request, render_template
load_dotenv()

app = flask.Flask(__name__)

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

@app.route("/")
@app.route("/report")
def report():
 return render_template("report.html")

@app.route("/liveView")
def liveView():
 return render_template("liveView.html")

tmp_time = 0

@app.route('/liveData')
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
    
@app.route('/drivers')
def get_drivers():
    sql = "SELECT DISTINCT driver_id FROM Driving_Record_B"
    cur.execute(sql)
    drivers = cur.fetchall()
    print ("drivers: ", drivers)
    return json.dumps(drivers)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000)