from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
import cv2

a = np.array([[1], [2], [3]])
b = np.array([[1, 1, 1], [3, 3, 3]])

c = pairwise_distances(a, metric="euclidean")
print(c)

img = cv2.imread('quickshift.png')
blur = cv2.GaussianBlur(img, (3,3), 0)
cv2.imwrite('blurred.png',blur)