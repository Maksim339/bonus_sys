import re
import os




tables = r'C:\Users\MVIDEO\PycharmProjects\bonus_sys\for_tables'
errors = r'C:\Users\MVIDEO\PycharmProjects\bonus_sys\for_errors'
bonus_box = r'C:\Users\MVIDEO\PycharmProjects\bonus_sys\for_bonus'


fds = os.listdir(tables)
fds1 = os.listdir(errors)
fds2 = os.listdir(bonus_box)



for img in fds:
    if re.search('.jpg', img):
        try:
            os.remove(os.path.join(tables, img))
        except Exception as e:
            print(e)


for image in fds1:
    if re.search('.jpg', image):
        try:
            os.remove(os.path.join(errors, image))
        except Exception as e:
            print(e)



for im in fds2:
    if re.search('.jpg', im):
        try:
            os.remove(os.path.join(bonus_box, im))
        except Exception as e:
            print(e)








