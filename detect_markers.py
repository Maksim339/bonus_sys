import cv2
import numpy as np





haystack_img = cv2.imread('kbs6.jpg', cv2.IMREAD_UNCHANGED)
needle_img = cv2.imread('template.jpg', cv2.IMREAD_UNCHANGED)


result = cv2.matchTemplate(haystack_img, needle_img, cv2.TM_SQDIFF_NORMED)


threshold = 0.05

locations = np.where(result <= threshold)

locations = list(zip(*locations[::-1]))
# print(locations)

if locations:
    print('Found needle.')

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]
    line_color = (0, 255, 0)
    line_type = cv2.LINE_4

    for loc in locations:
        top_left = loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        cv2.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)


    cv2.imwrite('test.jpg', haystack_img)
