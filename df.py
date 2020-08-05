import mysql.connector
import re
import pathlib
import os

path = pathlib.Path('result').absolute()
fds = os.listdir(path)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9f7S39D5!",
    database="mydatabase",
)

mycursor = mydb.cursor()
# #
# mycursor.execute("CREATE TABLE users (user_id VARCHAR(255), file_id VARCHAR(255))")
# mycursor.execute("CREATE TABLE results (user_id VARCHAR(255), file_id VARCHAR(255), value VARCHAR(10))")
# mycursor.execute("CREATE TABLE verified (user_id VARCHAR(255), file_id VARCHAR(255), value VARCHAR(10))")

def del_mac():
    if os.path.exists(path + ".DS_Store"):
        os.remove(path + ".DS_Store")


def insert_verified():
    for img in fds:
        print('fsdfsd')
        list = []
        list2 = []
        img = img.replace('.jpg', '')
        print(str(img))
        mycursor.execute("SELECT value, COUNT(*) FROM results WHERE file_id = '" + img + "'GROUP BY value")
        myresult = mycursor.fetchall()
        for i in range(len(myresult)):
            reg = re.compile("[),'(]")
            count = reg.sub("", str(myresult[i]))
            counter = int(count.split()[1])
            list.append(counter)
        for i in range(len(myresult)):
            list2.append((myresult[i])[0])
            print(list2)
        a = list.index(max(list))
        print(list2[a])

        sql = "INSERT INTO verified (filename, value) VALUES (%s, %s)"
        val = (str(img), str(list2[a]))
        mycursor.execute(sql, val)

    mydb.commit()

