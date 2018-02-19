import cv2
import os
import numpy as np
from collections import namedtuple


class BayesSpm:
    def __init__(self, skin_pixels, non_skin_pixels, appearances, appearances_as_skin):
        self.skin_pixels = skin_pixels
        self.non_skin_pixels = non_skin_pixels
        self.appearances = appearances
        self.appearances_as_skin = appearances_as_skin

Pixel = namedtuple("Pixel", ["R", "G", "B"])


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


def get_bayes_spm(path_pos, path_neg):
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


def calculate_pixel_probability_with_neighbours(pixel, spm):
    """
    Calculates the probability of a pixel being a skin pixel by getting the max probability from its neighbours

    :param pixel:
    :param spm:
    :return:
    """
    max_prob = 0
    for r_offset in range(-3, 3, 1):
        for g_offset in range(-3, 3, 1):
            for b_offset in range(-3, 3, 1):
                p = [pixel[0] + r_offset, pixel[1] + g_offset, pixel[2] + b_offset]
                prob = calculate_pixel_probability(p, spm)
                if prob > max_prob:
                    max_prob = prob
    return max_prob


def detect_skin(image, spm, threshold):
    new_image = image.copy()

    rows = image.shape[0]
    cols = image.shape[1]
    for x_pixel in range(rows):
        for y_pixel in range(cols):
            #prob = calculate_pixel_probability(image[x_pixel, y_pixel], spm)
            prob = calculate_pixel_probability_with_neighbours(image[x_pixel, y_pixel], spm)
            print(prob)
            if prob > threshold:
                new_image[x_pixel, y_pixel] = [0, 0, 0]

    return new_image

spm = get_bayes_spm('../../resources/input_data/skin/sfa/SKIN/35', '../../resources/input_data/skin/sfa/NS/35')

image = cv2.imread('../../resources/input_data/skin/girl_drink_3_5.png')
new_im = detect_skin(image, spm, 0.5)
cv2.imwrite('test_qs.png', new_im)