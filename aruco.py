import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import  matplotlib as mpl
import numpy as np
import re


def rotateImage(image, angle):
    (h, w) = image.shape[:2]
    (cX, CY) = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D((cX, CY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - CY
    rotated = cv2.warpAffine(image, M, (nW, nH))
    return rotated



dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
fig = plt.figure()
nx = 4
ny = 3
for i in range(1, nx*ny+1):
    ax = fig.add_subplot(ny,nx, i)
    img = aruco.drawMarker(dict,i, 700)
    plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
    ax.axis("off")
plt.savefig("markers1.jpg")


image = cv2.imread('right_test.png')
frame = rotateImage(image, -30)


original = np.copy(frame)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(gray, (3,3), 0)
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters =  aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict, parameters=parameters)
frame_markers = aruco.drawDetectedMarkers(original, corners, ids)
cv2.imwrite('test.jpg', frame_markers)





reg = re.compile('[] []')
id_marker = reg.sub('', str(ids)).split()
corner_id1 = int(id_marker.index('1'))
corner_id2 = int(id_marker.index('2'))
cornet_id3 = int(id_marker.index('3'))
corner_id4 = int(id_marker.index('4'))




##coord top left
id1 = corners[corner_id1]
reg = re.compile('[].[]')
count = reg.sub('', str(id1[0,3]) )
top_left1 = int(count.split()[0])
top_left2 = int(count.split()[1])
top_left = (int(top_left1), int(top_left2))
# print(corners)
# print(top_left)




###coords top right
id2 = corners[corner_id2]
reg = re.compile('[].[]')
count = reg.sub('', str(id2[0,2]) )
top_right1 = int(count.split()[0])
top_right2 = int(count.split()[1])
top_right = (int(top_right1), int(top_right2))
# print(id2)
# print(top_right)


###coords bottom left
id3 = corners[cornet_id3]
reg = re.compile('[].[]')
count = reg.sub('', str(id3[0,0]) )
bottom_left1 = int(count.split()[0])
bottom_left2 = int(count.split()[1])
bottom_left = (int(bottom_left1), int(bottom_left2))



###coords bottom right
id4 = corners[corner_id4]
reg = re.compile('[].[]')
count = reg.sub('', str(id4[0,1]) )
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



def order_points(pts):
    src_pts = np.zeros((4, 2), dtype = 'float32')
    # print(pts)
    s = np.sum(pts, axis=1)
    src_pts[0] = pts[np.argmin(s)]
    src_pts[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    src_pts[1] = pts[np.argmin(diff)]
    src_pts[3] = pts[np.argmax(diff)]
    return src_pts


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


warped = four_point_transform(frame_markers, pts)
# print(order_points(pts))
bonus = warped[47:, 531:605]
cv2.imwrite('warped.jpg', warped)

cv2.imwrite('bonus.jpg', bonus)