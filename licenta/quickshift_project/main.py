import cv2

from quickshift_project.quickshift import quickshift_algorithm

img = cv2.imread('../resources/input_data/PASCAL2007/people.jpg')
res = quickshift_algorithm(img, 2, 4, 1)
cv2.imwrite("people_2_4.png", res)

