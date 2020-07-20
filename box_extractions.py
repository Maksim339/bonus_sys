import cv2
from crop_table import crop_table
import numpy as np
from datetime import datetime
import time
import random
import os
from homography import align_kbs
import re

def box(img):
    path = r'/home/maksim/PycharmProjects/bonus_sys/kbs'
    path1 = r'/home/maksim/PycharmProjects/bonus_sys/Rows'

    image = img[50: ,580:660]
    original = np.copy(image)


    # Thresholding the image
    (thresh, img_bin) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Invert the image
    img_bin = 255 - img_bin
    # cv2.imwrite("test.jpg", img_bin)
    kernel_length = np.array(img).shape[1] // 80

    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))  # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))  # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    # cv2.imwrite("test.jpg",verticle_lines_img)# Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    # cv2.imwrite("test.jpg",horizontal_lines_img)



    edges = cv2.Laplacian(horizontal_lines_img, cv2.CV_8U)
    kernel1 = np.zeros((7, 31), np.uint8)
    kernel1[2, :] = 1
    eroded = cv2.morphologyEx(edges, cv2.MORPH_ERODE, kernel1)


    indices = np.nonzero(eroded)

    rows = np.unique(indices[0])

    filtered_rows = []
    for ii in range(len(rows)):
        if ii == 0:
            filtered_rows.append(rows[ii])
        else:
            if np.abs(rows[ii] - rows[ii - 1]) >= 18:
                filtered_rows.append(rows[ii])
    print(filtered_rows)
    a = 0
    try:
        for i in np.arange(len(filtered_rows) - 1):

            cv2.imwrite(os.path.join(path1, str(random.randint(1,1000)) + '.png'), original[filtered_rows[i]:filtered_rows[i + 1]])
    except IndexError:
        print('Thats all')


# alpha = 0.5
# beta = 1.0 - alpha# This function helps to add two image with specific weight parameter to get a third image as summation of two image.
# img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
# img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
# (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# cv2.imwrite("test.jpg",img_final_bin)
#
# def sort_contours(cnts, method="left-to-right"):
# 	reverse = False
# 	i = 0
# 	if method == "right-to-left" or method == "bottom-to-top":
# 		reverse = True
# 	if method == "top-to-bottom" or method == "bottom-to-top":
# 		i = 1
# 	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
# 	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
# 		key=lambda b:b[1][i], reverse=reverse))
# 	return (cnts, boundingBoxes)
#
#
#
# contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)# Sort all the contours by top to bottom.
# (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
#
# idx = 0
# for c in contours:
# 	x, y, w, h = cv2.boundingRect(c)# If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
# 	if (w == 80 and h > 20) and w > 3*h:
# 		idx += 1
# 		new_img = img[y:y+h, x:x+w]
# 		cv2.imwrite((os.path.join(path1, 'align_' + str(random.randint(1, 10000))) + '.jpg'), new_img)