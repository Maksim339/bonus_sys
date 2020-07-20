from __future__ import print_function
import cv2
import numpy as np
import random
import os
from _datetime import datetime
import time

start_time = datetime.now()
path1 = r'/home/maksim/PycharmProjects/bonus_sys/align'
MAX_FEATURES = 10000000
GOOD_MATCH_PERCENT = 0.15


def align_kbs(im1):
    im2 = cv2.imread('kbs6.jpg')
    image1 = cv2.resize(im1, (905,1280))
    image2 = cv2.resize(im2, (905,1280))
    im1Gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    matches.sort(key=lambda x: x.distance, reverse=False)
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    height, width, channels = im2.shape
    im1Reg = cv2.warpPerspective(im1, h, (width, height))
    # cv2.imwrite('aligned_kbs.jpg', im1Reg)
    cv2.imwrite((os.path.join(path1, 'align_' + str(random.randint(1, 10000))) + '.jpg'), im1Reg)
    return im1Reg

def align_work_list(im1):
    im1 = cv2.imread('work_list.jpg')
    im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    matches.sort(key=lambda x: x.distance, reverse=False)
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    height, width, channels = im2.shape
    im1Reg = cv2.warpPerspective(im1, h, (width, height))
    cv2.imwrite('aligned_kbs.jpg', im1Reg)
    return im1Reg




