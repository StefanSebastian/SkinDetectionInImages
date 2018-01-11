import cv2
from quickshift_project.algorithm.quickshift import quickshift_algorithm


img = cv2.imread('input_data/PASCAL2007/human_cat.jpg')
res = quickshift_algorithm(img, 3, 10, 1)
cv2.imwrite("human_cat_3_10.png", res)

