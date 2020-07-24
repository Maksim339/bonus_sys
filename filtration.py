import re
import os
import cv2


def filtration():
    bonus_box = r'C:\Users\MVIDEO\PycharmProjects\bonus_sys\for_bonus'
    fds2 = os.listdir(bonus_box)

    for img in fds2:
        if re.search('.jpg', img):
            try:
                image = cv2.imread(os.path.join(bonus_box, img))
                if image.shape[0] > 50:
                    os.remove(os.path.join(bonus_box, img))
            except Exception as e:
                print(e)