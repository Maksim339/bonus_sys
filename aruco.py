import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import re
import os
from defs import four_point_transform, remove, rows, filtration
import pathlib

path = pathlib.Path('aruco.py').parent.absolute()  # путь к проекту
path1 = pathlib.Path('from').absolute()  # путь к директории, из которой считываются документы
fds = os.listdir("from")


a = 0
b = 0
c = 0
d = None

errors = None
bonus_box = None
tables = None

top_left = None
top_right = None
bottom_left = None
bottom_right = None

# создание папок для сохранения вырезанного пространства между маркерами: tables
# для ошибок: errors
# для хранения изображений с цифрами : bonus_box
try:
    tables = os.path.join(path, "for_tables")
    os.mkdir(tables)
except Exception as e:
    print(e)

try:
    errors = os.path.join(path, "for_errors")
    os.mkdir(errors)
except Exception as e:
    print(e)

try:
    bonus_box = os.path.join(path, "for_bonus")
    os.mkdir(bonus_box)
except Exception as e:
    print(e)


remove(tables, errors, bonus_box)

# создание словаря для идентификации маркеров
dict = aruco.Dictionary_get(aruco.DICT_6X6_50)
fig = plt.figure()
nx = 4
ny = 3
for i in range(1, nx * ny + 1):
    ax = fig.add_subplot(ny, nx, i)
    img = aruco.drawMarker(dict, i, 700)
    plt.imshow(img, cmap=mpl.cm.gray, interpolation="nearest")
    ax.axis("off")
plt.savefig("markers2.jpg")


for img in fds:
    if re.search(".jpg", img):
        frame_markers = None
        try:
            image = cv2.imread(os.path.join(path1, img))  # считывание изобр.
            frame = cv2.resize(image, (905, 1280))  # приведение к единому размеру
            original = np.copy(frame)  # сохранение оригинала
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # переведение изобр. в оттенки серого
            blur = cv2.GaussianBlur(gray, (1, 1), 0)  # размытие изобр, изобр. с парметрами больше (1,1) не распознаются
            # распознавание маркеров
            aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
            parameters = aruco.DetectorParameters_create()
            corners, ids, rejectedImgPoints = aruco.detectMarkers(
                blur, dict, parameters=parameters
            )
            frame_markers = aruco.drawDetectedMarkers(original, corners, ids)
            # cv2.imwrite('test.jpg', frame_markers)

            # работа с переменной ids, которая хранит массив с уникальными id маркеров
            # присваивание каждому углу правильный id
            reg = re.compile("[] []")
            id_marker = reg.sub("", str(ids)).split()
            corner_id1 = int(id_marker.index("1"))
            corner_id2 = int(id_marker.index("2"))
            cornet_id3 = int(id_marker.index("3"))
            corner_id4 = int(id_marker.index("4"))

            # обработка рабочих листов
            if re.search("worker_list", img):

                # coord top left
                id1 = corners[corner_id1]
                reg = re.compile("[].[]")
                count = reg.sub("", str(id1[0, 3]))  # берется нужная координата маркера (у каждого маркера 4 коорд.)
                top_left1 = int(count.split()[0])
                top_left2 = int(count.split()[1])
                top_left = (int(top_left1), int(top_left2))

                # coord top right
                id2 = corners[corner_id2]
                reg = re.compile("[].[]")
                count = reg.sub("", str(id2[0, 2]))
                top_right1 = int(count.split()[0])
                top_right2 = int(count.split()[1])
                top_right = (int(top_right1), int(top_right2))

                # coord bottom left
                id3 = corners[cornet_id3]
                reg = re.compile("[].[]")
                count = reg.sub("", str(id3[0, 0]))
                bottom_left1 = int(count.split()[0])
                bottom_left2 = int(count.split()[1])
                bottom_left = (int(bottom_left1), int(bottom_left2))

                # coord bottom right
                id4 = corners[corner_id4]
                reg = re.compile("[].[]")
                count = reg.sub("", str(id4[0, 1]))
                bottom_right1 = int(count.split()[0])
                bottom_right2 = int(count.split()[1])
                bottom_right = (int(bottom_right1), int(bottom_right2))

                # print('top_left', top_left)
                # print('top_right', top_right)
                # print('bottom_left', bottom_left)
                # print('bottom_right', bottom_right)

                pts = [top_left, top_right, bottom_left, bottom_right]

                table = four_point_transform(frame_markers, pts)
                # нормирование размеров изображения
                table_normal = cv2.resize(table, (829, 842))
                # сохранение вырезанного куска
                cv2.imwrite(
                    (os.path.join(tables, str("table_") + str(a)) + ".jpg"), table_normal
                )
                first_bon = table_normal[247:297, :90]  # вырезка крайнего левого блока со знач. бонуса
                second_bon = table_normal[247:297, 423:507]  # вырезка крайнего правого блока со знач. бонуса
                # сохранение блока с бонусом
                cv2.imwrite(
                    (os.path.join(bonus_box, str("work_b_1_") + str(b)) + ".jpg"),
                    first_bon,
                )
                cv2.imwrite(
                    (os.path.join(bonus_box, str("work_b_2_") + str(b)) + ".jpg"),
                    second_bon,
                )
                a += 1
                b += 1

            # обработка кбс листов
            if re.search("kbs", img):

                # coord top left
                id1 = corners[corner_id1]
                reg = re.compile("[].[]")
                count = reg.sub("", str(id1[0, 3]))
                top_left1 = int(count.split()[0])
                top_left2 = int(count.split()[1])
                top_left = (int(top_left1), int(top_left2))
                # print(corners)
                # print(top_left)

                # coord top right
                id2 = corners[corner_id2]
                reg = re.compile("[].[]")
                count = reg.sub("", str(id2[0, 2]))
                top_right1 = int(count.split()[0])
                top_right2 = int(count.split()[1])
                top_right = (int(top_right1), int(top_right2))
                # print(id2)
                # print(top_right)

                # coord bottom left
                id3 = corners[cornet_id3]
                reg = re.compile("[].[]")
                count = reg.sub("", str(id3[0, 0]))
                bottom_left1 = int(count.split()[0])
                bottom_left2 = int(count.split()[1])
                bottom_left = (int(bottom_left1), int(bottom_left2))

                # coord bottom right
                id4 = corners[corner_id4]
                reg = re.compile("[].[]")
                count = reg.sub("", str(id4[0, 1]))
                bottom_right1 = int(count.split()[0])
                bottom_right2 = int(count.split()[1])
                bottom_right = (int(bottom_right1), int(bottom_right2))
                # print(bottom_right)
                # print(id4)

                # print('top_left', top_left)
                # print('top_right', top_right)
                # print('bottom_left', bottom_left)
                # print('bottom_right', bottom_right)
                pts = [top_left, top_right, bottom_left, bottom_right]

                table = four_point_transform(frame_markers, pts)
                bonus_normal = cv2.resize(table, (830, int(table.shape[0])))
                cv2.imwrite(
                    (os.path.join(tables, str("table_") + str(a)) + ".jpg"), bonus_normal
                )
                bonus_normal = cv2.resize(table, (830, table.shape[0]))
                # print(table.shape[0])
                bonus = bonus_normal[63:, 602:685]
                cv2.imwrite(
                    (os.path.join(bonus_box, str("bonus_1_") + str(b)) + ".jpg"), bonus
                )
                a += 1
                b += 1
        except Exception as e:
            print(e)
            print("Marker isnt detect")
            cv2.imwrite(
                (os.path.join(errors, str("errors_") + str(c)) + ".jpg"), frame_markers
            )
            c += 1

os.remove("markers2.jpg")  # удаление словаря маркеров

d = rows(bonus_box)

filtration(bonus_box, d)
