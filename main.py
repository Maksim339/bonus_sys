from columns import col
import os
import re
import cv2
from homography import align_kbs
from datetime import datetime
import time
import numpy as np
from crop_table import crop_table
from box_extractions import box


path = r'C:\Users\MVIDEO\PycharmProjects\bonus_sys\kbs'
path1 = r'C:\Users\MVIDEO\PycharmProjects\bonus_sys\Rows'
fds = sorted(os.listdir(path))
fds1 = sorted(os.listdir(path1))


start_time = datetime.now()


for image in fds:
    if re.match(r'kbs', image):
        img = cv2.imread(os.path.join(path, image))
        align = align_kbs(img)
        crop = crop_table(align)
        img = cv2.imread('output2.png', cv2.IMREAD_GRAYSCALE)
        if img is None:
            img = cv2.imread('output1.png', cv2.IMREAD_GRAYSCALE)
        print(img.shape[0])
        box(img)
        try:
            os.remove('output1.png')
            os.remove('output2.png')
        except Exception as e:
            print(e)
a = 0
for image1 in fds1:
    if re.match(r'\d', image1):
        img = cv2.imread(os.path.join(path1, image1))
        if img.shape[0] < 40 or img.shape[0] > 46:
            print('lox')
            stroka = str(image1)
            os.remove(os.path.join(path1, image1))
#
        
time.sleep(5)
print(datetime.now() - start_time)
