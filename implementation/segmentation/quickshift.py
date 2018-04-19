from math import exp

import numpy as np

from segmentation.superpixel import Superpixel
from segmentation.utils import point_distance_2d, point_distance_3d, feature_distance_5d
from utils.log import LogFactory
from utils.tuples import Position


class QuickshiftSegmentation:
    def __init__(self, with_position, sigma, tau, logger=LogFactory.get_default_logger()):
        self.with_position = with_position
        self.sigma = sigma
        self.tau = tau
        self.logger = logger

    def apply(self, image):
        """
        Returns a segmented image
        """
        self.logger.log("\nCalculating densities")
        densities = self.__compute_density(image)

        self.logger.log("\nLinking neighbours")
        parents = self.__link_neighbours(image, densities)

        self.logger.log("\nCreating new image")
        return self.__get_image_with_superpixels(image, parents)

    def get_superpixels(self, image):
        """
        Returns the superpixels
        """
        self.logger.log("\nCalculating densities")
        densities = self.__compute_density(image)

        self.logger.log("\nLinking neighbours")
        parents = self.__link_neighbours(image, densities)

        self.logger.log("\nExtracting super pixels")
        return self.__extract_superpixels(image, parents)

    def __extract_superpixels(self, image, parents):
        super_pixels = {}

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if parents[i, j][0] == 0 and parents[i, j][1] == 0:
                    pos = Position(X=i, Y=j)
                    super_pixels[pos] = Superpixel([i, j], image)

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                x_pixel, y_pixel = self.__get_root_pixel(parents, i, j)
                pos = Position(X=x_pixel, Y=y_pixel)
                super_pixels[pos].add_pixel([i, j])

        return super_pixels

    def __compute_density(self, image):
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

                self.logger.print_progress_pixel(x_pixel, y_pixel, rows, cols)

                # get neighbourhood window
                x_upper = x_pixel - 3 * self.sigma
                y_upper = y_pixel - 3 * self.sigma
                x_lower = x_pixel + 3 * self.sigma
                y_lower = y_pixel + 3 * self.sigma

                # iterate neighbourhood
                for x_candidate in range(x_upper, x_lower + 1):
                    for y_candidate in range(y_upper, y_lower + 1):
                        # check bounds
                        if 0 <= x_candidate < rows and 0 <= y_candidate < cols:
                            if point_distance_2d(x_pixel, y_pixel, x_candidate, y_candidate) <= 3 * self.sigma:
                                point = image[x_candidate, y_candidate]
                                # distance between pixel values ; f[x] - f[n]
                                if self.with_position == 0:
                                    distance = point_distance_3d(point[0], point[1], point[2],
                                                                 pixel[0], pixel[1], pixel[2])
                                else:
                                    distance = feature_distance_5d(point[0], point[1], point[2],
                                                                   pixel[0], pixel[1], pixel[2],
                                                                   x_candidate, y_candidate, x_pixel, y_pixel)
                                # update density ; d += e^(-d^2 / 2 * sigma^2)
                                densities[x_pixel, y_pixel] += exp((-(distance ** 2)) / (2 * self.sigma * self.sigma))
        return densities

    def __link_neighbours(self, image, densities):
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
                self.logger.print_progress_pixel(x_pixel, y_pixel, rows, cols)

                # get neighbourhood window
                x_upper = x_pixel - self.tau
                y_upper = y_pixel - self.tau
                x_lower = x_pixel + self.tau
                y_lower = y_pixel + self.tau

                # iterate neighbourhood
                for x_candidate in range(x_upper, x_lower + 1):
                    for y_candidate in range(y_upper, y_lower + 1):
                        # check bounds
                        if 0 <= x_candidate < rows and 0 <= y_candidate < cols:
                            # distance between pixel and neighbour coordinates
                            distance = point_distance_2d(x_pixel, y_pixel, x_candidate, y_candidate)
                            if distance <= self.tau:
                                # if the neighbour has a higher density and is closer to the current pixel
                                # or is the first neighbour with a higher density
                                if densities[x_candidate, y_candidate] > densities[x_pixel, y_pixel] and \
                                        ((distances[x_pixel, y_pixel] > distance) or (
                                                    distances[x_pixel, y_pixel] == 0)):
                                    distances[x_pixel, y_pixel] = distance
                                    parents[x_pixel, y_pixel] = np.array([x_candidate, y_candidate])
        return parents

    def __get_root_pixel(self, parents, x_pixel, y_pixel):
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
            return self.__get_root_pixel(parents, x_parent, y_parent)

    def __get_image_with_superpixels(self, image, parents):
        """
        Creates a new image starting from the given one, where each pixel is replaced with the root of the tree

        :param image: given image
        :param parents: parents matrix
        :return: an image as numpy array
        """
        new_image = image.copy()
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                x_pixel, y_pixel = self.__get_root_pixel(parents, i, j)
                parent_pixel = image[x_pixel, y_pixel]
                new_image[i, j] = parent_pixel
        return new_image
