import cv2
import os
from collections import namedtuple

from skin_probability_map.bayes import config


class BayesSpm:
    """
    Class that encapsulates a bayes Skin Probability Map
    """

    def __init__(self, skin_pixels, non_skin_pixels, appearances, appearances_as_skin):
        self.skin_pixels = skin_pixels
        self.non_skin_pixels = non_skin_pixels
        self.appearances = appearances
        self.appearances_as_skin = appearances_as_skin


"""
Named tuple representing a pixel ; used as a key for Bayes Map
"""
Pixel = namedtuple("Pixel", ["R", "G", "B"])


def load_images_from_folder(folder):
    """
    Utility method that loads all images from a folder

    :param folder:
    :return:
    """
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


def get_bayes_spm(path_pos, path_neg):
    """
    Calculates Bayes SPM
    :param path_pos: path to positive examples
    :param path_neg: path to negative examples
    :return:
    """
    appearances = {}
    appearances_as_skin = {}
    skin_pixels = 0
    non_skin_pixels = 0

    skin_images = load_images_from_folder(path_pos)
    for image in skin_images:
        rows = image.shape[0]
        cols = image.shape[1]
        for x_pixel in range(rows):
            for y_pixel in range(cols):
                skin_pixels += 1
                pixel = image[x_pixel, y_pixel]
                p = Pixel(R=pixel[0], G=pixel[1], B=pixel[2])
                if p in appearances:
                    appearances[p] += 1
                    appearances_as_skin[p] += 1
                else:
                    appearances[p] = 1
                    appearances_as_skin[p] = 1

    non_skin_images = load_images_from_folder(path_neg)
    for image in non_skin_images:
        rows = image.shape[0]
        cols = image.shape[1]
        for x_pixel in range(rows):
            for y_pixel in range(cols):
                non_skin_pixels += 1
                pixel = image[x_pixel, y_pixel]
                p = Pixel(R=pixel[0], G=pixel[1], B=pixel[2])
                if p in appearances:
                    appearances[p] += 1
                else:
                    appearances[p] = 1

    return BayesSpm(skin_pixels, non_skin_pixels, appearances, appearances_as_skin)


def calculate_pixel_probability(pixel, spm):
    """
    Calculates the probability that the given pixel is a skin pixel

    uses the formula p = P(X|S) * P(S) / P(X)
    where S represents the prob of a pixel being a skin pixel ; X the probability of getting the selected pixel
    and P(X|S) the prob of finding this pixel given skin

    :param pixel:
    :param spm:
    :return:
    """
    p = Pixel(R=pixel[0], G=pixel[1], B=pixel[2])

    if p not in spm.appearances_as_skin:
        return 0

    px = spm.appearances[p] / (spm.skin_pixels + spm.non_skin_pixels)
    ps = spm.skin_pixels / (spm.skin_pixels + spm.non_skin_pixels)
    pxs = spm.appearances_as_skin[p] / spm.skin_pixels
    return (pxs * ps) / px


"""
Global variable ; map that caches pixel probabilities
"""
pixel_probability_cache = {}


def calculate_pixel_probability_with_neighbours(pixel, spm):
    """
    Calculates the probability of a pixel being a skin pixel by getting the max probability from its neighbours

    :param pixel:
    :param spm:
    :return:
    """
    max_prob = 0
    area = config.neighbour_area
    for r_offset in range(-area, area, 1):
        for g_offset in range(-area, area, 1):
            for b_offset in range(-area, area, 1):
                p = [pixel[0] + r_offset, pixel[1] + g_offset, pixel[2] + b_offset]
                prob = calculate_pixel_probability(p, spm)
                if prob > max_prob:
                    max_prob = prob
    return max_prob


def detect_skin(image, spm, threshold):
    new_image = image.copy()
    new_image[:] = (255, 255, 255)  # make image white
    cv2.addWeighted(image, 0.4, new_image, 1 - 0.4, 0, new_image)  # overlay transparent img

    rows = image.shape[0]
    cols = image.shape[1]
    for x_pixel in range(rows):
        for y_pixel in range(cols):
            pixel = image[x_pixel, y_pixel]

            # check cache
            p = Pixel(R=pixel[0], G=pixel[1], B=pixel[2])
            if p in pixel_probability_cache:
                prob = pixel_probability_cache[p]
            else:
                # calculate using strategy given as param
                if config.with_neighbours == 0:
                    prob = calculate_pixel_probability(pixel, spm)
                else:
                    prob = calculate_pixel_probability_with_neighbours(pixel, spm)
                pixel_probability_cache[p] = prob

            print(prob)
            if prob > threshold:
                new_image[x_pixel, y_pixel] = [0, 0, 0]
    return new_image
