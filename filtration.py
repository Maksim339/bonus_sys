# import re
# import os
# import cv2
#
#
# def filtration(path):
#     fds2 = os.listdir(path)
#
#     for img in fds2:
#         if re.search('.jpg', img):
#             try:
#                 image = cv2.imread(os.path.join(path, img))
#                 if image.shape[0] > 50 or image.shape[0] < 40:
#                     i = 0
#                     os.remove(os.path.join(path, img))
#                     i += 1
#
#             except Exception as e:
#                 print(e)