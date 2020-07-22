import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import  matplotlib as mpl
import numpy as np





aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

fig = plt.figure()
nx = 4
ny = 3
for i in range(1, nx*ny+1):
    ax = fig.add_subplot(ny,nx, i)
    img = aruco.drawMarker(aruco_dict,i, 700)
    plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
    ax.axis("off")

plt.savefig("markers.jpg")


image = cv2.imread('lox.png')
frame = image[115:1323, 200:1110]
# cv2.imwrite('frame.jpg', fr)
# frame = cv2.imread('frame.jpg')
original = np.copy(frame)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(gray, (3,3), 0)
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters =  aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
frame_markers = aruco.drawDetectedMarkers(original, corners, ids)
cv2.imwrite('test.jpg', frame_markers)

###coord top left
# top_left1 = str(corners[1])[46:48]
# top_left2 = str(corners[1])[50:53]
# top_left = (int(top_left1), int(top_left2))
#
#
#
#
# print(top_left)