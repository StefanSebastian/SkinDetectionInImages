import cv2
import numpy as np
from math import sqrt

# read initial image
img = cv2.imread('input_data/cat.jpg')
print('Shape of image' + str(img.shape))
print('Shape of pixel' + str(img[0][0].shape))


def point_distance(x1, y1, x2, y2):
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    return sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


def point_distance_3d(x1, y1, z1, x2, y2, z2):
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    z1 = int(z1)
    z2 = int(z2)
    return sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2) + ((z2 - z1) ** 2))


def compute_density(image, sigma):
    rows = image.shape[0]
    cols = image.shape[1]
    densities = np.zeros((rows, cols))
    print(densities.shape)

    for x_pixel in range(rows):
        for y_pixel in range(cols):
            # for each pixel
            pixel = image[x_pixel, y_pixel]

            densities[x_pixel, y_pixel] = 0

            progress = x_pixel * cols + y_pixel
            if progress % 300 == 0:
                progress = progress / (rows * cols)
                progress *= 100
                print(progress, "%")

            # get upper corner of window
            x_upper = x_pixel - 5 * sigma
            y_upper = y_pixel - 5 * sigma

            # get lower corner of window
            x_lower = x_pixel + 5 * sigma
            y_lower = y_pixel + 5 * sigma

            # iterate neighbourhood
            for x_candidate in range(x_upper, x_lower + 1):
                for y_candidate in range(y_upper, y_lower + 1):
                    # check bounds
                    if 0 <= x_candidate < rows and 0 <= y_candidate < cols:
                        if point_distance(x_pixel, y_pixel, x_candidate, y_candidate) <= 3 * sigma:
                            point = image[x_candidate, y_candidate]
                            # distance between pixel values ; f[x] - f[n]
                            distance = point_distance_3d(point[0], point[1], point[2], pixel[0], pixel[1], pixel[2])
                            densities[x_pixel, y_pixel] += np.exp((-(distance ** 2)) / (2 * sigma * sigma))
    return densities


def link_neighbours(image, tau, densities):
    rows = image.shape[0]
    cols = image.shape[1]
    distances = np.zeros((rows, cols))
    parents = np.zeros((rows, cols, 2))

    for x_pixel in range(rows):
        for y_pixel in range(cols):
            # for each pixel
            progress = x_pixel * cols + y_pixel
            if progress % 300 == 0:
                progress = progress / (rows * cols)
                progress *= 100
                print(progress, "%")

            # get upper corner of window
            x_upper = x_pixel - tau
            y_upper = y_pixel - tau

            # get lower corner of window
            x_lower = x_pixel + tau
            y_lower = y_pixel + tau

            # iterate neighbourhood
            for x_candidate in range(x_upper, x_lower + 1):
                for y_candidate in range(y_upper, y_lower + 1):
                    # check bounds
                    if 0 <= x_candidate < rows and 0 <= y_candidate < cols:
                        distance = point_distance(x_pixel, y_pixel, x_candidate, y_candidate)
                        if distance <= tau:
                            if densities[x_candidate, y_candidate] > densities[x_pixel, y_pixel] and \
                                    ((distances[x_pixel, y_pixel] > distance) or (distances[x_pixel, y_pixel] == 0)):
                                distances[x_pixel, y_pixel] = distance
                                parents[x_pixel, y_pixel] = np.array([x_candidate, y_candidate])
    return parents


def get_new_image(image, parents):
    new_image = image.copy()

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            parent = parents[i, j]
            print("parent" + str(parent))
            x_parent = int(parent[0])
            y_parent = int(parent[1])
            parent_pixel = image[x_parent, y_parent]
            print("parent: " + str(parent_pixel))
            if x_parent != 0 and y_parent != 0:
                new_image[i, j] = parent_pixel
    return new_image


def get_root_parent(image, parents, x, y):
    parent = parents[x, y]
    x_parent = int(parent[0])
    y_parent = int(parent[1])
    # when pixel is root
    if x_parent == 0 and y_parent == 0:
        return image[x, y]
    else:
        return get_root_parent(image, parents, x_parent, y_parent)


'''
goes all the way to root parent
'''


def get_new_image2(image, parents):
    new_image = image.copy()

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            parent_pixel = get_root_parent(image, parents, i, j)
            new_image[i, j] = parent_pixel
    return new_image


print("Compute densities")
densitiesC = compute_density(img, 2)
print("Get parents")
parentsC = link_neighbours(img, 10, densitiesC)
img2 = get_new_image2(img, parentsC)
cv2.imwrite('quickshift.png', img2)
