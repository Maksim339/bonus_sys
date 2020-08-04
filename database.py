import mysql.connector
import re
import os
import pathlib

def database():
    def values(value):
        """
        Функция распределяет классифицированные человеком изображения по классам для обучения нейоросети
        :param value: название класса
        """
        fds = os.listdir("for_bonus")
        path1 = pathlib.Path('for_bonus').absolute()
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
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="9f7S39D5!",
          database="mydatabase"
        )

        mycursor = mydb.cursor()

        if len(value) > 3:
            print('is str')
            # запрос
            mycursor.execute("SELECT name FROM bonussys WHERE value = 'invalid'")
        else:
            mycursor.execute("SELECT name FROM bonussys WHERE value = " + str(value))



        myresult = mycursor.fetchall()
        for x in myresult:
            reg = re.compile("[),'(]")
            filename = reg.sub("", str(x))
            # print(filename)
            # for img in fds:

            #     if re.search(filename + '.jpg', img):
            os.replace(os.path.join(path1, filename), classes + '/' + filename)



    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="9f7S39D5!",
      database="mydatabase"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT value, COUNT(*) FROM bonussys GROUP BY value")
    myresult = mycursor.fetchall()
    print(myresult)
    reg = re.compile("[),'(]")

    for i in range(len(myresult)):
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
