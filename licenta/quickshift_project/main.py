import cv2

from quickshift_project.quickshift import quickshift_algorithm

img = cv2.imread('../resources/input_data/PASCAL2007/girl_drink.jpg')
res = quickshift_algorithm(img, 3, 5, 1)
cv2.imwrite("girl_drink_3_5.png", res)

