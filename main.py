import mysql.connector
import os
import df
import pathlib
import shutil
import re

path = pathlib.Path('for_bonus').absolute()
resultpath = pathlib.Path('result').absolute()
fds = os.listdir(resultpath)
print(fds)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9f7S39D5!",
    database="mydatabase",
    port='3306'
)

mycursor = mydb.cursor()

#
# def del_mac():
#     if os.path.exists(path + ".DS_Store"):
#         os.remove(path + ".DS_Store")


# # --СКОЛЬКО РАЗ БЫЛО ОТРАВЛЕННО ИЗОБРАЖЕНИЕ.

def remove_file(file_id):
    files = os.listdir(path)
    mycursor.execute("SELECT file_id, COUNT(*) FROM users GROUP BY file_id")
    myresult = mycursor.fetchall()
    for x in myresult:
        count = x[-1]
        if count > 2:
            print('2')
            filename = str(file_id) + '.jpg'
            print('3')
            shutil.copyfile(path + filename, resultpath + filename)
            print('4')
            # if os.path.exists(path + filename):
            os.remove(path + filename)
            print('5')
            sql = "DELETE FROM users WHERE file_id = '{}'".format(file_id)
            mycursor.execute(sql)
            mydb.commit()
            print(mycursor.rowcount, "record(s) deleted")

            # print(count)


def remove_bd(file_id):
    # remove_file(file_id)
    mycursor.execute("SELECT file_id, COUNT(*) FROM users GROUP BY file_id")
    myresult = mycursor.fetchall()
    for x in myresult:
        count = x[-1]
        if count > 1:
            sql = "DELETE FROM users WHERE file_id = '{}'".format(file_id)
            mycursor.execute(sql)
            mydb.commit()
            print(mycursor.rowcount, "record(s) deleted")


# remove_bd(65)

def insert_sql(user_id, file_id):
    sql = "INSERT INTO users (user_id, file_id) VALUES (%s, %s)"
    val = (user_id, file_id)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


def validation(user_id, file_id):
    mycursor.execute("SELECT * FROM users WHERE user_id = '{}' AND file_id = '{}'".format(user_id, file_id))
    myresult = mycursor.fetchone()
    # print(myresult)
    return myresult


# validation(949191326, 188)
# #
# sql = "DELETE FROM users WHERE user_id = '604652371'"
# mycursor.execute(sql)
# mydb.commit()
# print(mycursor.rowcount, "record(s) deleted")


def check(user_id, file_id):
    files = os.listdir(path)
    if os.path.exists(path + ".DS_Store"):
        os.remove(path + ".DS_Store")
    bd_valid = validation(user_id, file_id=file_id)  # Проверка, есть ли айди юзера и фото в БД
    num = 0
    while True:
        if bd_valid is None:  # НЕ НАШЕЛ В БАЗЕ!
            if os.path.exists(path + ".DS_Store"):
                os.remove(path + ".DS_Store")
            file_id = file_id.split('.jpg')[0]
            return 'ok', file_id

        elif bd_valid:  # НАШЕЛ В БАЗЕ!
            if os.path.exists(path + ".DS_Store"):
                os.remove(path + ".DS_Store")
            try:
                file = files[num]
                file_id = file.split('.jpg')[0]
                bd = validation(user_id, file_id=file_id)
                if bd is None:
                    return 'ok', file_id
                else:
                    num += 1
            except IndexError:
                return 'finish'


# check(222, 188)

# validation(222,188)

def remove5(file_id):
    files = os.listdir(path)
    # mycursor.execute("SELECT file_id, COUNT(*) as count FROM users GROUP BY file_id")
    mycursor.execute("SELECT file_id, COUNT(*) FROM users WHERE file_id = '{}'".format(file_id))
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

# remove5('05571edda43fba70df828cd197b10a6f')