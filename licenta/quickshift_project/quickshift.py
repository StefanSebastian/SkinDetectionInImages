from math import sqrt, exp

import numpy as np

from utils import utils
from quickshift_project.superpixel import Superpixel, SuperpixelFeatures
from utils.utils import Position


def quickshift_algorithm(image, sigma, tau, with_position=0):
    """
    Apply quickshift algorithm and return the resulting image

    :param image:
    :param sigma:
    :param tau:
    :param with_position:
    :return:
    """
    print("\nCalculating densities")
    densities = __compute_density(image, sigma, with_position)

    print("\nLinking neighbours")
    parents = __link_neighbours(image, tau, densities)

    print("\nCreating new image")
    return __get_image_with_superpixels(image, parents)


def point_distance_2d(x1, y1, x2, y2):
    """
    Euclidean distance between 2 points in 2d space
    """
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    return sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


def feature_distance_3d(x1, y1, z1, x2, y2, z2):
    """
    Euclidean distance between 2 points in 3d space

    x, y, z should be the rgb values
    """
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    z1 = int(z1)
    z2 = int(z2)
    return sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2) + ((z2 - z1) ** 2))


def feature_distance_5d(r1, g1, b1, r2, g2, b2, x1, y1, x2, y2):
    """
    Euclidean distance between 2 points in 5d space

    r, g, b should be the rgb coordinates ; which are scaled
    x,y are the positions
    """
    r1 = 0.5 * int(r1)
    r2 = 0.5 * int(r2)
    g1 = 0.5 * int(g1)
    g2 = 0.5 * int(g2)
    b1 = 0.5 * int(b1)
    b2 = 0.5 * int(b2)
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    return sqrt(((r2 - r1) ** 2) + ((g2 - g1) ** 2) + ((b2 - b1) ** 2) + ((x2 - x1) ** 2) + ((y2 - y1) ** 2))


def __compute_density(image, sigma, with_position):
    """
    Compute the Parzen density for each pixel

    :param image: given image
    :param sigma: sigma parameter
    :return: a matrix the size of the image with all densities
    """
    rows = image.shape[0]
    cols = image.shape[1]
    densities = np.zeros((rows, cols))

    # iterate all pixels
    for x_pixel in range(rows):
        for y_pixel in range(cols):
            pixel = image[x_pixel, y_pixel]

            utils.print_progress_pixel(x_pixel, y_pixel, rows, cols)

            # get neighbourhood window
            x_upper = x_pixel - 3 * sigma
            y_upper = y_pixel - 3 * sigma
            x_lower = x_pixel + 3 * sigma
            y_lower = y_pixel + 3 * sigma

            # iterate neighbourhood
            for x_candidate in range(x_upper, x_lower + 1):
                for y_candidate in range(y_upper, y_lower + 1):
                    # check bounds
                    if 0 <= x_candidate < rows and 0 <= y_candidate < cols:
                        if point_distance_2d(x_pixel, y_pixel, x_candidate, y_candidate) <= 3 * sigma:
                            point = image[x_candidate, y_candidate]
                            # distance between pixel values ; f[x] - f[n]
                            if with_position == 0:
                                distance = feature_distance_3d(point[0], point[1], point[2], pixel[0], pixel[1],
                                                               pixel[2])
                            else:
                                distance = feature_distance_5d(point[0], point[1], point[2], pixel[0], pixel[1],
                                                               pixel[2],
                                                               x_candidate, y_candidate, x_pixel, y_pixel)
                            # update density ; d += e^(-d^2 / 2 * sigma^2)
                            densities[x_pixel, y_pixel] += exp((-(distance ** 2)) / (2 * sigma * sigma))
    return densities


def __link_neighbours(image, tau, densities):
    """
    Links each pixel to the nearest pixel on a tau radius that has a higher density

    :param image: given image
    :param tau: area of neighbourhood
    :param densities: density matrix for each pixel
    :return: a matrix with the coordinates of each parent ; coordinates are (0, 0) for roots
    """
    rows = image.shape[0]
    cols = image.shape[1]

    # matrix of distance ; each position will contain the distance between the pixel at the current position
    # and the closest pixel with a higher density in the tau radius
    distances = np.zeros((rows, cols))

    # matrix of parents ; each position will contain the parent of the corresponding pixel
    parents = np.zeros((rows, cols, 2))

    # iterate pixels
    for x_pixel in range(rows):
        for y_pixel in range(cols):
            utils.print_progress_pixel(x_pixel, y_pixel, rows, cols)

            # get neighbourhood window
            x_upper = x_pixel - tau
            y_upper = y_pixel - tau
            x_lower = x_pixel + tau
            y_lower = y_pixel + tau

            # iterate neighbourhood
            for x_candidate in range(x_upper, x_lower + 1):
                for y_candidate in range(y_upper, y_lower + 1):
                    # check bounds
                    if 0 <= x_candidate < rows and 0 <= y_candidate < cols:
                        # distance between pixel and neighbour coordinates
                        distance = point_distance_2d(x_pixel, y_pixel, x_candidate, y_candidate)
                        if distance <= tau:
                            # if the neighbour has a higher density and is closer to the current pixel
                            # or is the first neighbour with a higher density
                            if densities[x_candidate, y_candidate] > densities[x_pixel, y_pixel] and \
                                    ((distances[x_pixel, y_pixel] > distance) or (distances[x_pixel, y_pixel] == 0)):
                                distances[x_pixel, y_pixel] = distance
                                parents[x_pixel, y_pixel] = np.array([x_candidate, y_candidate])
    return parents


def __get_root_pixel(parents, x_pixel, y_pixel):
    """
    Gets the root of the tree the pixel with the coordinates (x_pixel, y_pixel) is in

    :param parents: parents matrix
    :param x_pixel: row of current pixel
    :param y_pixel: col of current pixel
    :return:
    """
    parent = parents[x_pixel, y_pixel]
    x_parent = int(parent[0])
    y_parent = int(parent[1])
    # when pixel is root
    if x_parent == 0 and y_parent == 0:
        return x_pixel, y_pixel
    else:
        return __get_root_pixel(parents, x_parent, y_parent)


def __get_image_with_superpixels(image, parents):
    """
    Creates a new image starting from the given one, where each pixel is replaced with the root of the tree

    :param image: given image
    :param parents: parents matrix
    :return: an image as numpy array
    """
    new_image = image.copy()
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            x_pixel, y_pixel = __get_root_pixel(parents, i, j)
            parent_pixel = image[x_pixel, y_pixel]
            new_image[i, j] = parent_pixel
    return new_image


def get_superpixels(image, sigma, tau, with_position=0):
    print("\nCalculating densities")
    densities = __compute_density(image, sigma, with_position)

    print("\nLinking neighbours")
    parents = __link_neighbours(image, tau, densities)

    print("\nExtracting super pixels")
    return extract_superpixels(image, parents)


def extract_superpixels(image, parents):
    super_pixels = {}

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if parents[i, j][0] == 0 and parents[i, j][1] == 0:
                pos = Position(X=i, Y=j)
                super_pixels[pos] = Superpixel([i, j], image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            x_pixel, y_pixel = __get_root_pixel(parents, i, j)
            pos = Position(X=x_pixel, Y=y_pixel)
            super_pixels[pos].add_pixel([i, j])

    for key in super_pixels:
        features = SuperpixelFeatures.calculate_features(super_pixels[key])
        super_pixels[key].set_features(features)

    return super_pixels
