import cv2
from quickshift_project.algorithm.quickshift import quickshift_algorithm

img = cv2.imread('input_data/PASCAL2007/people.jpg')
res = quickshift_algorithm(img, 3, 10)
cv2.imwrite('quickshift_project.png', res)