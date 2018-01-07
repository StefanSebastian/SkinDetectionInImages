from sklearn.metrics.pairwise import pairwise_distances
import numpy as np

a = np.array([[1], [2], [3]])
b = np.array([[1, 1, 1], [3, 3, 3]])

c = pairwise_distances(a, metric="euclidean")
print(c)