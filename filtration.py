import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt
# import matplotlib as mpl
import numpy as np
import re
import os
from defs import four_point_transform, remove, rows, filtration

try:
    os.remove('errors_0.jpg')
except Exception as e:
    print(e)
dict = aruco.Dictionary_get(aruco.DICT_6X6_1000)
fig = plt.figure()
nx = 4
ny = 3
for i in range(1, nx*ny+1):
    ax = fig.add_subplot(ny,nx, i)
    img = aruco.drawMarker(dict,i, 700)
    # plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
    ax.axis("off")
plt.savefig("markers2.jpg")

a = 0
b = 0
c = 0

frame_markers = None
try:
    image = cv2.imread('worker_list3.jpg')
    frame = cv2.resize(image, (905, 1280))
    original = np.copy(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (1,1), 0)
    # cv2.imwrite('test.jpg', blur)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(original, corners, ids)
    cv2.imwrite('look.jpg', frame_markers)








    reg = re.compile('[] []')
    id_marker = reg.sub('', str(ids)).split()
    corner_id1 = int(id_marker.index('1'))
    corner_id2 = int(id_marker.index('2'))
    cornet_id3 = int(id_marker.index('3'))
    corner_id4 = int(id_marker.index('4'))




    ##coord top left
    id1 = corners[corner_id1]
    reg = re.compile('[].[]')
    count = reg.sub('', str(id1[0,2]) )
    top_left1 = int(count.split()[0])
    top_left2 = int(count.split()[1])
    top_left = (int(top_left1), int(top_left2))
    # print(corners)
    # print(top_left)




    ###coords top right
    id2 = corners[corner_id2]
    reg = re.compile('[].[]')
    count = reg.sub('', str(id2[0,3]) )
    top_right1 = int(count.split()[0])
    top_right2 = int(count.split()[1])
    top_right = (int(top_right1), int(top_right2))
    # print(id2)
    # print(top_right)




    ###coords bottom left
    id3 = corners[cornet_id3]
    reg = re.compile('[].[]')
    count = reg.sub('', str(id3[0,1]) )
    bottom_left1 = int(count.split()[0])
    bottom_left2 = int(count.split()[1])
    bottom_left = (int(bottom_left1), int(bottom_left2))




    ###coords bottom right
    id4 = corners[corner_id4]
    reg = re.compile('[].[]')
    count = reg.sub('', str(id4[0,0]) )
    bottom_right1 = int(count.split()[0])
    bottom_right2 = int(count.split()[1])
    bottom_right = (int(bottom_right1), int(bottom_right2))
    # print(bottom_right)
    # print(id4)
    #
    # print('top_left', top_left)
    # print('top_right', top_right)
    # print('bottom_left', bottom_left)
    # print('bottom_right', bottom_right)

    pts = [top_left, top_right, bottom_left, bottom_right]

    table = four_point_transform(frame_markers, pts)
    table_normal = cv2.resize(table, (678, table.shape[0]))
    cv2.imwrite(str('table_') + str(a) + '.jpg', table)
    first_bon = table_normal[:65,:75]
    cv2.imwrite('test.jpg', first_bon)
    second_bon = table_normal[:65,339:420]
    cv2.imwrite('test2.jpg', second_bon)

    # cv2.imwrite((os.path.join(bonus_box, str('bonus_') + str(b)) + '.jpg'), bonus)
    a += 1
    b += 1

except Exception as e:
    print(e)
    print('Marker isnt detect')
    # cv2.imwrite(str('errors_') + str(c) + '.jpg', frame_markers)
    c += 1


