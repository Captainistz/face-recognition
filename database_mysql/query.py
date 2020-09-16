import mysql.connector as con
# require : pip install mysql-connector
from datetime import date, datetime

db = con.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "utd_affairs"
)

sql = db.cursor()

def check(user):
    _check = "SELECT schoolCheck FROM student WHERE student_id = " + str(user)
    sql.execute(_check)
    result = sql.fetchone()
    if result[0]==1:
        return 1
    else:
        return 0

def student_scan_in(user, date, time, status):
    scanin_query = "INSERT INTO scan_in_logs (user, date, time, status) VALUES (%s, %s, %s, %s)"
    scanin_data = (user, date, time, status)
    boolcheck_query = "UPDATE student SET schoolCheck = %s WHERE student_id = %s"
    boolcheck_data = (1, user)
    
    sql.execute(scanin_query, scanin_data)
    sql.execute(boolcheck_query, boolcheck_data)
    db.commit()

def _insert(id, name, lastname, room, class_number):
    addstudent_query = "INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s)"
    addstudent_data = (id, name, lastname, room, class_number, 0)
    sql.execute(addstudent_query, addstudent_data)
    db.commit()
#student_scan_in(34864, today_date, now_time, "normal") #-- test case for scan in
#check(34864)
"""
addstudent_query = "INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s, %s)"
addstudent_data = (34808, '1234', 'นายกัปตัน', 'พึ่งเป็นสุข', '5.1', '4', '5')
sql.execute(addstudent_query, addstudent_data)
"""
if __name__ == "__main__":
    _insert(34808, 'นายกัปตัน', 'พึ่งเป็นสุข', '5.1', '4')