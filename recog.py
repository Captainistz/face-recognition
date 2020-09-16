import os
import cv2
import json


def recog_face(name, face_id):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    with open("json/user.json") as f:
        users = json.loads(f.read())

    print("\n [INFO] Initializing face capture. Look the camera and wait ...")

    count = 0

    os.mkdir('./dataset/' + name + '.' + str(face_id))

    while(True):

        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            count += 1
            cv2.imwrite("dataset/" + str(name) + '.' + str(face_id) +
                        '/' + str(count) + ".jpg", gray[y:y+h, x:x+w])

            cv2.imshow('image', img)

        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break
        elif count >= 100:
            break

    with open("json/user.json", "w") as f:
        json.dump(users, f, indent=4, sort_keys=True)

    print("\n [INFO] Exiting Program")
    cam.release()
    cv2.destroyAllWindows()
