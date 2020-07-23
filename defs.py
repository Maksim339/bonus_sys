import cv2
import numpy as np


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


def order_points(pts):
    src_pts = np.zeros((4, 2), dtype='float32')
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
