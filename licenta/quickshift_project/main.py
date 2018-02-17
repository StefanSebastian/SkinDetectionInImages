import cv2

from quickshift_project.quickshift import quickshift_algorithm

img = cv2.imread('../resources/input_data/PASCAL2007/baby.jpg')
res = quickshift_algorithm(img, 2, 4, 1)

for i in range(2, 5):
    for j in range(4, 8):
        res = quickshift_algorithm(img, i, j)
        cv2.imwrite("baby_" + str(i) + "-" + str(j) + ".png", res)
#cv2.imwrite("people_2_4.png", res)

