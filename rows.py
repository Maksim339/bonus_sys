# import cv2
# import numpy as np
# import os
# import random
# import re


# def rows(path1):
#     fds = os.listdir(path1)
#
#     a = 0
#
#     for img in fds:
#         if re.search('bonus_', img):
#             image = cv2.imread(os.path.join(path1, img), cv2.IMREAD_GRAYSCALE)
#             original = np.copy(image)
#
#             i = None
#
#             (thresh, img_bin) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#             img_bin = 255 - img_bin
#
#             kernel_length = np.array(image).shape[1] // 90
#             horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
#
#             # cv2.imwrite("test.jpg",vertical_lines_img)
#             img_temp2 = cv2.erode(img_bin, horizontal_kernel, iterations=3)
#             horizontal_lines_img = cv2.dilate(img_temp2, horizontal_kernel, iterations=3)
#             # cv2.imwrite("test.jpg",horizontal_lines_img)
#
#             edges = cv2.Laplacian(horizontal_lines_img, cv2.CV_8U)
#             kernel1 = np.zeros((7, 31), np.uint8)
#             kernel1[2, :] = 1
#             eroded = cv2.morphologyEx(edges, cv2.MORPH_ERODE, kernel1)
#
#             indices = np.nonzero(eroded)
#             rows = np.unique(indices[0])
#
#             filtered_rows = []
#             for ii in range(len(rows)):
#                 if ii == 0:
#                     filtered_rows.append(rows[ii])
#                 else:
#                     if np.abs(rows[ii] - rows[ii - 1]) >= 6:
#                         filtered_rows.append(rows[ii])
#             print(filtered_rows)
#
#             try:
#                 for i in np.arange(len(filtered_rows) - 1):
#                     cv2.imwrite((os.path.join(path1, str('bonus_box_') + str(i + a)) + '.jpg'), original[filtered_rows[i]:filtered_rows[i + 1]])
#             except IndexError:
#                 print('Thats all')
#
#             a = a + i
#
#             if image.shape[0] > 50:
#                 os.remove(os.path.join(path1, img))





