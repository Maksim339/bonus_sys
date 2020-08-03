import mysql.connector
import re
import os
import pathlib


def values(value):
    """
    Функция распределяет классифицированные человеком изображения по классам для обучения нейоросети
    :param value:
    """
    fds = os.listdir("from")
    path1 = pathlib.Path('from').absolute()
    path = pathlib.Path('aruco.py').parent.absolute()
    clas = None
    classes = None
    try:
        clas = os.path.join(path, "class")
        os.mkdir(clas)
    except Exception as e:
        print(e)
    try:
        classes = os.path.join(clas, str(value))
        os.mkdir(classes)
    except Exception as e:
        print(e)

    i = 0
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="9f7S39D5!",
      database="mydatabase"
    )

    mycursor = mydb.cursor()

    if type(value) is str:
        print('is str')
        mycursor.execute("SELECT address FROM customers WHERE value = 'invalid'")
    else:
        mycursor.execute("SELECT address FROM customers WHERE value = " + str(value))


    myresult = mycursor.fetchall()
    for x in myresult:
        reg = re.compile("[),'(]")
        filename = reg.sub("", str(x))
        for img in fds:
            if re.search(filename, img):
                os.replace(os.path.join(path1, img), classes + '/' + filename)
                i += 1

