import mysql.connector
import re
import pathlib
import os
path = pathlib.Path('fff').absolute()
fds = os.listdir(path)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9f7S39D5!",
    database="mydatabase"
)

mycursor = mydb.cursor()
mycursor.execute("DROP TABLE bonussys")
mycursor.execute("CREATE TABLE bonussys (name VARCHAR(255), address VARCHAR(255), value VARCHAR(7))")
sql = "INSERT INTO bonussys (name, address, value) VALUES (%s, %s, %s)"
val = [
  ('hundred.3.jpg', 'hundred.3.jpg', '12'),
  ('hundred.5.jpg', 'Apple st 652', '45'),
  ('hundred.6.jpg', 'Mountain 21', '100'),
  ('hundred.3.jpg', 'Valley 345', '45'),
  ('hundred.5.jpg', 'Ocean blvd 2', 'invalid'),
  ('hundred.6.jpg', 'Green Grass 1', '45'),
  ('hundred.3.jpg', 'Sky st 331', '11'),
  ('hundred.3.jpg', 'One way 98', '11'),
  ('hundred.3.jpg', 'Yellow Garden 2', '45'),
  ('hundred.8.jpg', 'Park Lane 38', '100'),
  ('hundred.3.jpg', 'Central st 954' , '100'),
  ('hundred.3.jpg', 'Main Road 989', '100'),
  ('hundred.3.jpg', 'Sideway 1633', '45')
]
list = []
mycursor.executemany(sql, val)
# mycursor.execute("SELECT * FROM bonussys WHERE name = 'hundred.3.jpg'")
for img in fds:
    print(str(img))
    mycursor.execute("SELECT value, COUNT(*) FROM bonussys WHERE name = '" + img + "'GROUP BY value")
    myresult = mycursor.fetchall()
    count = None
    for i in range(len(myresult)):
        reg = re.compile("[),'(]")
        count = reg.sub("", str(myresult[i]))
        counter = int(count.split()[1])
        list.append(counter)
        print(count)
    print(max(list))

mydb.commit()

