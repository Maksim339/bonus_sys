import cv2
import numpy as np
import os
import re


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array(
        [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
        dtype="float32",
    )

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped


def order_points(pts):
    src_pts = np.zeros((4, 2), dtype="float32")
    # print(pts)
    s = np.sum(pts, axis=1)
    src_pts[0] = pts[np.argmin(s)]
    src_pts[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    src_pts[1] = pts[np.argmin(diff)]
    src_pts[3] = pts[np.argmax(diff)]
    return src_pts


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


def remove(tables, errors, bonus_box):

    fds = os.listdir(tables)
    fds1 = os.listdir(errors)
    fds2 = os.listdir(bonus_box)

    for img in fds:
        if re.search(".jpg", img):
            try:
                os.remove(os.path.join(tables, img))
            except Exception as e:
                print(e)

    for image in fds1:
        if re.search(".jpg", image):
            try:
                os.remove(os.path.join(errors, image))
            except Exception as e:
                print(e)

    for im in fds2:
        if re.search(".jpg", im):
            try:
                os.remove(os.path.join(bonus_box, im))
            except Exception as e:
                print(e)


def filtration(path):
    fds2 = os.listdir(path)

    for img in fds2:
        if re.search("bonus", img):
            try:
                image = cv2.imread(os.path.join(path, img))
                if image.shape[0] > 50 or image.shape[0] < 40:
                    i = 0
                    os.remove(os.path.join(path, img))
                    i += 1

            except Exception as e:
                print(e)


def rows(path1):
    fds = os.listdir(path1)

    a = 0

    for img in fds:
        if re.search("bonus_", img):
            image = cv2.imread(os.path.join(path1, img), cv2.IMREAD_GRAYSCALE)
            original = np.copy(image)

            i = None

            (thresh, img_bin) = cv2.threshold(
                image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
            )
            img_bin = 255 - img_bin

            kernel_length = np.array(image).shape[1] // 90
            horizontal_kernel = cv2.getStructuringElement(
                cv2.MORPH_RECT, (kernel_length, 1)
            )

            # cv2.imwrite("test.jpg",vertical_lines_img)
            img_temp2 = cv2.erode(img_bin, horizontal_kernel, iterations=3)
            horizontal_lines_img = cv2.dilate(
                img_temp2, horizontal_kernel, iterations=3
            )
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
                    if np.abs(rows[ii] - rows[ii - 1]) >= 6:
                        filtered_rows.append(rows[ii])
            print(filtered_rows)

            try:
                for i in np.arange(len(filtered_rows) - 1):
                    cv2.imwrite(
                        (os.path.join(path1, str("bonus_box_") + str(i + a)) + ".jpg"),
                        original[filtered_rows[i] : filtered_rows[i + 1]],
                    )
            except IndexError:
                print("Thats all")

            a = a + i

            if image.shape[0] > 50:
                os.remove(os.path.join(path1, img))
