import json
import train
import recog
import database_mysql.query

with open('json/user.json') as f:
    inf = json.loads(f.read())

studentid = input("Enter your studentID: ")
name = input("Enter your name: ")
lastname = input("Enter your lastname: ")
_class = input('Enter your class : ')
class_number = input('Enter your class number : ')


if not name in inf:
    inf[str(studentid)] = {}
    inf[str(studentid)]["name"] = name
    database_mysql.query._insert(studentid, name, lastname, _class, class_number)

    recog.recog_face(name, studentid)

    if train.face_train() == 1:
        with open('json/user.json', 'w') as f:
            json.dump(inf, f, indent=4, sort_keys=True)
