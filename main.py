import os
from cv2 import cv2
import json
import numpy as np
import time 
import urllib.request
from datetime import date, datetime
import database_mysql.query
import line_noti
import url_cfg

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

id = 0

with open("json/user.json") as f:
    users = json.loads(f.read())

while True:
    imgResp=urllib.request.urlopen(url_cfg.url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)

    today = date.today()
    now = datetime.now()
    today_date = today.strftime("%d/%m/%Y") # ex. 11/09/2020
    now_time = now.strftime("%H:%M:%S") # ex. 21:53:20
    status = "normal"
    status_thai = ""

    #ret, img = cam.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
        #minSize=(int(minW), int(minH)),
    )

    for(x, y, w, h) in faces:

        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        if (confidence < 100):
            name = users[str(id)]["name"]
            confidence = "  {0}%".format(round(100 - confidence))
            
            if database_mysql.query.check(id) == 0:
                database_mysql.query.student_scan_in(id, str(today_date), str(now_time), str(status))
                if status == "normal":
                    status_thai = "อุณหภูมิปกติ"
                elif status == "hightemp":
                    status_thai = "อุณหภูมิสูงเกินปกติ"
                else:
                    print('[ERROR] Hmm.. status string is not match.')
                line_noti.notifyFile(id, str(status_thai))
            #else:
            #    time.sleep(0.02)
            #    print(str(id) + " is already scanned in before.")
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(img, str(name), (x+5, y-5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x+5, y+h-5),
                    font, 1, (255, 255, 0), 1)

    cv2.imshow('image', img)

    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

print("\n [INFO] Exiting Program")
#cam.release()
cv2.destroyAllWindows()
