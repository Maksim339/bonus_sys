import numpy as np
import cv2
from homography import align_kbs
from crop_table import crop_table
import os
import random
import shutil


def col(img):
    path = r'/home/maksim/PycharmProjects/bonus_sys'
    path1 = r'/home/maksim/PycharmProjects/bonus_sys/Rows'
    # try:
    #     shutil.rmtree(r'/home/maksim/PycharmProjects/bonus_sys/Rows')
    #     print('removed')
    # except Exception as e:
    #     print(e)


    try:
        path1 = os.path.join(path, 'Rows')
        os.mkdir(path1)
    except Exception as e:
        print(e)
    aligned = align_kbs(img)
    crop_table(aligned)
    image = cv2.imread('output1.png', cv2.IMREAD_GRAYSCALE)
    # os.remove('output1.png')
    image = img[55:, 580:660]
    original = np.copy(image)

    (thresh, img_bin) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_bin = 255 - img_bin
    cv2.imwrite("test.jpg", img_bin)
    kernel_length = np.array(img).shape[1] // 80

    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,
                                                                 kernel_length))
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    # cv2.imwrite("test.jpg",verticle_lines_img)# Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    # cv2.imwrite("test.jpg", horizontal_lines_img)
    edges = cv2.Laplacian(image, cv2.CV_8U)
    kernel = np.zeros((7, 31), np.uint8)
    kernel[2, :] = 1
    eroded = cv2.morphologyEx(edges, cv2.MORPH_ERODE, kernel)

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

    try:
        for i in np.arange(len(filtered_rows) - 1):
            cv2.imwrite(os.path.join(path1, 'rows' + str(i) + '.png'), original[filtered_rows[i]:filtered_rows[i + 1]])
    except IndexError:
        print('Thats all')

    # rows_2(cv2.imread('test.jpg'))

    # len_col = crop_img.shape[0] / 47
    # count = 0
    # i = 0
    # a = 48
    # while count < (int(len_col) - 1):
    #     crop_col = crop_img[i:a]
    #
    #     if crop_col.shape[0] == 44:
    #         cv2.imwrite((os.path.join(path1, 'box_' + str(random.randint(1,10000))) + '.jpg'), crop_col)
    #         print(crop_col.shape[1])
    #     i += 48
    #     a += 47
    #     count += 1






