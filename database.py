import mysql.connector
import re
import os
import pathlib
import pygments

result = r'/home/maksim/PycharmProjects/bonus_sys/result/'
fds = os.listdir(result)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydatabase"
)

mycursor = mydb.cursor()


def insert_verified():
    for img in fds:
        list = []
        list2 = []
        img = img.replace('.jpg', '')
        # print(str(img))
        mycursor.execute("SELECT value, COUNT(*) FROM results WHERE file_id = '" + img + "'GROUP BY value")
        myresult = mycursor.fetchall()
        for i in range(len(myresult)):
            reg = re.compile("[),'(]")
            count = reg.sub("", str(myresult[i]))
            counter = int(count.split()[1])
            list.append(counter)
        for i in range(len(myresult)):
            list2.append((myresult[i])[0])
            # print(list2)
        a = list.index(max(list))
        # print(list2[a])
        mycursor.execute("SELECT file_id, COUNT(*) FROM verified WHERE file_id = '" + img + "'")
        myresult = mycursor.fetchall()
        if ((myresult[0])[1]) > 0:
            break
        else:
            sql = "INSERT INTO verified (file_id, value) VALUES (%s, %s)"
            val = (str(img), str(list2[a]))
            mycursor.execute(sql, val)

    mydb.commit()

def database():
    def values(value):
        """
        Функция распределяет классифицированные человеком изображения по классам для обучения нейоросети
        :param value: название класса
        """
        # fds = os.listdir("for_bonus")
        result = pathlib.Path('result').absolute()
        path = pathlib.Path('aruco.py').parent.absolute()
        clas = None
        classes = None
        try:
            clas = os.path.join(path, "class")
            os.mkdir(clas)
            print('ffefqe')
        except Exception as e:
            print(e)
        try:
            classes = os.path.join(clas, value)
            os.mkdir(classes)
        except Exception as e:
            print(e)

        i = 0
        # подключение к базе данных

        if len(value) > 3:
            print('is str')
            # запрос
            mycursor.execute("SELECT file_id FROM verified WHERE value = 'invalid'")
        else:
            mycursor.execute("SELECT file_id FROM verified WHERE value = " + str(value))



        myresult = mycursor.fetchall()
        print(myresult)

        for x in myresult:
            reg = re.compile("[),'(]")
            filename = reg.sub("", str(x))
            # print(filename)
            # for img in fds:

            #     if re.search(filename + '.jpg', img):
            try:
                os.replace(os.path.join(result, filename + '.jpg'), classes + '/' + filename + '.jpg')
            except Exception:
                print('result is empty')


    mycursor.execute("SELECT value, COUNT(*) FROM verified GROUP BY value")
    myresult = mycursor.fetchall()
    print(myresult)
    reg = re.compile("[),'(]")

    for i in range(len(myresult)):
        print(myresult[i])
        count = reg.sub("", str(myresult[i]))
        unique = count.split()[0]
        counter = int(count.split()[1])
        if counter > 0:
            try:
                values(unique)
            except Exception as e:
                print(e)
                values(unique)
        else:
            print('Количество изображений с распознанным значением', unique, 'должно быть не меньше 100')


def insert_value(user_id, file_id, value):
    try:
        if len(str(value)) > 3 or str(value) == '000' or int(value) > 100:
            value = 'invalid'
        print(int(value))
    except ValueError:
        value = 'invalid'
    except Exception as e:
        print(e)
        value = 'invalid'


    sql = "INSERT INTO results (user_id, file_id, value) VALUES (%s, %s, %s)"
    try:
        valid = int(value)
        val = (user_id, file_id, int(value))
    except ValueError:
        val = (user_id, file_id, value)


    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserter!")


def insert_verified():
    for img in fds:
        list = []
        list2 = []
        img = img.replace('.jpg', '')
        # print(str(img))
        mycursor.execute("SELECT value, COUNT(*) FROM results WHERE file_id = '" + img + "'GROUP BY value")
        myresult = mycursor.fetchall()
        for i in range(len(myresult)):
            reg = re.compile("[),'(]")
            count = reg.sub("", str(myresult[i]))
            counter = int(count.split()[1])
            list.append(counter)
        for i in range(len(myresult)):
            list2.append((myresult[i])[0])
            # print(list2)
        a = list.index(max(list))
        # print(list2[a])
        mycursor.execute("SELECT file_id, COUNT(*) FROM verified WHERE file_id = '" + img + "'")
        myresult = mycursor.fetchall()
        if ((myresult[0])[1]) > 0:
            break
        else:
            sql = "INSERT INTO verified (file_id, value) VALUES (%s, %s)"
            val = (str(img), str(list2[a]))
            mycursor.execute(sql, val)

    mydb.commit()
