import cv2
import numpy as np
import os
import random
import re



path1 = r'C:\Users\MVIDEO\PycharmProjects\bonus_sys\for_bonus'
fds = os.listdir(path1)

a = 0


def rows(image, a):
    original = np.copy(image)

    i = None
    # Thresholding the image
    (thresh, img_bin) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Invert the image
    img_bin = 255 - img_bin
    # cv2.imwrite("test.jpg", img_bin)
    kernel_length = np.array(image).shape[1] // 70

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
            if np.abs(rows[ii] - rows[ii - 1]) >= 25:
                filtered_rows.append(rows[ii])
    print(filtered_rows)

    try:

        for i in np.arange(len(filtered_rows) - 1):
            cv2.imwrite((os.path.join(path1, str('bonus_box_') + str(a)) + '.jpg'), original[filtered_rows[i]:filtered_rows[i + 1]])
            a += 1


    except IndexError:
        print('Thats all')
    return a

        

for img in fds:
    if re.search('bonus_', img):
        image = cv2.imread(os.path.join(path1, img), cv2.IMREAD_GRAYSCALE)
        a = rows(image, 0)
        rows(image, a)

