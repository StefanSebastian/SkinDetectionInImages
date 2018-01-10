import cv2
from quickshift_project.algorithm.quickshift import quickshift_algorithm

sigma = [2, 3, 4]
tau = [5, 10, 20]

img = cv2.imread('input_data/PASCAL2007/people.jpg')

for i in range(3):
    for j in range(3):
        res = quickshift_algorithm(img, sigma[i], tau[j], 1)
        cv2.imwrite('people' + str(sigma[i]) + "_" + str(tau[j]) + ".png", res)