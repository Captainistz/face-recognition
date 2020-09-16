import os
from datetime import datetime
import mysql.connector as con
import database_mysql.query as dbfile

url = 'https://notify-api.line.me/api/notify'
token = 'WJpRrzHr3Y8WW3XPyf7nXzbyjSsZdF1OFX5X3Q6VgUs'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

def notifyFile(studentid, status):
    name = "SELECT name FROM student WHERE student_id = " + str(studentid)
    dbfile.sql.execute(name)
    name_result = dbfile.sql.fetchone()
    lastname = "SELECT lastname FROM student WHERE student_id = " + str(studentid)
    dbfile.sql.execute(lastname)
    lastname_result = dbfile.sql.fetchone()
    dbfile.db.commit()
    text = " [DEBUG]" + "\n" + str(studentid) + " | " + name_result[0] +  ' ' + lastname_result[0] + "\n" + "เวลา : " + datetime.now().strftime("%H:%M:%S") + "\n" + "สถานะ : " + status
    #print(text) #--debugging name and lastname
    payload = {'message':text}
    return _lineNotify(payload)

def _lineNotify(payload, file=None):
    import requests
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization':'Bearer ' + token}
    return requests.post(url, headers=headers , data = payload)