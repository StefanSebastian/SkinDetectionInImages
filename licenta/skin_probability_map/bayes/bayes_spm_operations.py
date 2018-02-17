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


def get_bayes_spm(path):
    appearances = {}
    appearances_as_skin = {}
    skin_pixels = 0
    non_skin_pixels = 0

    skin_images = load_images_from_folder(path + '/positive')
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

    non_skin_images = load_images_from_folder(path + '/negative')
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
    p = Pixel(R=pixel[0], G=pixel[1], B=pixel[2])

    if p not in spm.appearances_as_skin:
        return 0

    px = spm.appearances[p] / (spm.skin_pixels + spm.non_skin_pixels)
    ps = spm.skin_pixels / (spm.skin_pixels + spm.non_skin_pixels)
    pxs = spm.appearances_as_skin[p] / spm.skin_pixels
    return (pxs * ps) / px


def detect_skin(image, spm, threshold):
    new_image = image.copy()

    rows = image.shape[0]
    cols = image.shape[1]
    for x_pixel in range(rows):
        for y_pixel in range(cols):
            prob = calculate_pixel_probability(image[x_pixel, y_pixel], spm)
            print(prob)
            if prob > threshold:
                new_image[x_pixel, y_pixel] = [0, 0, 0]

    return new_image

spm = get_bayes_spm('../../resources/input_data/skin')

image = cv2.imread('../../resources/input_data/skin/people3_5.png')
new_im = detect_skin(image, spm, 0.6)
cv2.imwrite('test.png', new_im)