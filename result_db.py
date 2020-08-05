import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9f7S39D5!",
    database="mydatabase"
)

mycursor = mydb.cursor()


# Добавление в БД "result" значений: user_id | file_id | value
def insert_value(user_id, file_id, value):
    if len(str(value)) > 3:
        value = 'invalid'
    sql = "INSERT INTO results (user_id, file_id, value) VALUES (%s, %s, %s)"
    val = (user_id, file_id, value)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserter!")