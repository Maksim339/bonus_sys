import cv2
import numpy as np






img = cv2.imread('kbs6_turn.jpg', cv2.IMREAD_UNCHANGED)
template = cv2.imread('template.jpg', cv2.IMREAD_UNCHANGED)

# print(img)

result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)


threshold = 0.95

locations = np.where(result <= threshold)

locations = list(zip(*locations[::-1]))
# print(locations)

if locations:
    print('Found markers')

    needle_w = template.shape[1]
    needle_h = template.shape[0]
    line_color = (200, 50, 255)
    line_type = cv2.LINE_4

    for loc in locations:
        top_left = loc

        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        cv2.rectangle(img, top_left, bottom_right, line_color, line_type)
        # print(top_left)

        print(bottom_right)
#
# print(top_left)
# print(bottom_right)
top = (692, 579)
bottom = (777, 364)
print(type(top))
cv2.rectangle(img, top, bottom, line_color, line_type)

cv2.imwrite('test.jpg', img)




