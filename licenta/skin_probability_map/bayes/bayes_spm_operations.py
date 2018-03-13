"""
planning to remove this module and use train + detect modules instead
"""

import cv2
import numpy as np

from skin_probability_map.bayes import config
from utils import utils, serialization
from utils.utils import Pixel


class BayesSpmComponents:
    """
    Class that encapsulates components of a bayes Skin Probability Map
    """

    def __init__(self, skin_pixels, non_skin_pixels, appearances, appearances_as_skin):
        """
        Components of a Bayes spm

        :param skin_pixels: number of skin pixels in training set
        :param non_skin_pixels: number of nonskin pixels in training set
        :param appearances: map<Pixel, int> ; number of appearances of each pixel
        :param appearances_as_skin: map<Pixel, int> ; number of appearances of each pixel as a skin pixel
        """
        self.skin_pixels = skin_pixels
        self.non_skin_pixels = non_skin_pixels
        self.appearances = appearances
        self.appearances_as_skin = appearances_as_skin


def train_model():
    """
    Calculates the bayes components and serializes them

    :return:
    """
    if config.database == 'compaq':
        bayes_spm_components = __get_bayes_spm_components_compaq(config.path_compaq, config.color_space)
    else:
        bayes_spm_components = __get_bayes_spm_components_sfa(config.path_pos, config.path_neg, config.color_space)
    serialization.save_object(bayes_spm_components, config.path_models + '/' + config.selected_model)
    return bayes_spm_components


def detect_skin_spm(image, model_path, threshold, with_neighbours, neighbour_area):
    bayes_spm_components = serialization.load_object(model_path)
    return __detect_skin(image, bayes_spm_components, threshold, with_neighbours, neighbour_area)


def __detect_skin(image, bayes_spm_components, threshold, with_neighbours=1, neighbour_area=8):
    """
    Builds spm as needed and calculates pixel probabilities

    Caches pixel probabilities for faster calculations

    :param neighbour_area:
    :param with_neighbours:
    :param image:
    :param bayes_spm_components:
    :param threshold:
    :return:
    """
    new_image = image.copy()
    new_image[:] = (255, 255, 255)  # make image white
    cv2.addWeighted(image, 0.4, new_image, 1 - 0.4, 0, new_image)  # overlay transparent img

    rows = image.shape[0]
    cols = image.shape[1]
    for x_pixel in range(rows):
        for y_pixel in range(cols):
            utils.print_progress_pixel(x_pixel, y_pixel, rows, cols)

            pixel = image[x_pixel, y_pixel]

            # check cache
            p = Pixel(F1=pixel[0], F2=pixel[1], F3=pixel[2])
            if p in pixel_probability_cache:
                prob = pixel_probability_cache[p]
            else:
                # calculate using strategy given as param
                if with_neighbours == 0:
                    prob = __calculate_pixel_probability(pixel, bayes_spm_components)
                else:
                    prob = __calculate_pixel_probability_with_neighbours(pixel, bayes_spm_components, neighbour_area)
                pixel_probability_cache[p] = prob

            if prob > threshold:
                new_image[x_pixel, y_pixel] = [0, 0, 0]
    return new_image


def __get_bayes_spm_components_compaq(path_train, color_space):
    """
    Extract bayes spm components from compaq db
    each image has a corresponding mask
    a black pixel on a mask means not skin while a white pixel means skin
    :param path_train:
    :return:
    """
    appearances = {}
    appearances_as_skin = {}
    skin_pixels = 0
    non_skin_pixels = 0

    images = utils.load_images_from_folder(path_train + "/" + "train_images")
    masks = utils.load_images_from_folder(path_train + "/" + "train_masks")

    for current_index in range(len(images)):
        utils.print_progress(current_index, len(images))
        image = images[current_index]
        mask = masks[current_index]

        image = utils.convert_color(image, color_space)

        img_skin_pixels, img_non_skin_pixels = __get_components_from_image_mask(image, mask, appearances, appearances_as_skin)
        skin_pixels += img_skin_pixels
        non_skin_pixels += img_non_skin_pixels
    return BayesSpmComponents(skin_pixels, non_skin_pixels, appearances, appearances_as_skin)


def __get_components_from_image_mask(image, mask, appearances, appearances_as_skin):
    """
    Extracts bayes components from an image given a mask
    :param image:
    :param mask:
    :param appearances:
    :param appearances_as_skin:
    :return:
    """
    skin_pixels = 0
    non_skin_pixels = 0
    rows = image.shape[0]
    cols = image.shape[1]
    for x_pixel in range(rows):
        for y_pixel in range(cols):
            pixel = image[x_pixel, y_pixel]
            p = Pixel(F1=pixel[0], F2=pixel[1], F3=pixel[2])
            if np.all(mask[x_pixel, y_pixel] == 0):  # not skin
                non_skin_pixels += 1
                if p in appearances:
                    appearances[p] += 1
                else:
                    appearances[p] = 1
            else:
                skin_pixels += 1

                if p in appearances:
                    appearances[p] += 1
                else:
                    appearances[p] = 1

                if p in appearances_as_skin:
                    appearances_as_skin[p] += 1
                else:
                    appearances_as_skin[p] = 1
    return skin_pixels, non_skin_pixels


def __get_bayes_spm_components_sfa(path_pos, path_neg, color_space):
    """
    Calculates Bayes SPM components from sfa ; skin images and non skin images are saved in separate folders

    :param path_pos: path to positive examples
    :param path_neg: path to negative examples
    :return:
    """
    appearances = {}
    appearances_as_skin = {}
    skin_pixels = 0
    non_skin_pixels = 0

    print("Calculating bayes spm components for skin images")
    skin_images = utils.load_images_from_folder(path_pos)
    for image in skin_images:
        image = utils.convert_color(image, color_space)

        rows = image.shape[0]
        cols = image.shape[1]
        for x_pixel in range(rows):
            for y_pixel in range(cols):
                skin_pixels += 1
                pixel = image[x_pixel, y_pixel]
                p = Pixel(F1=pixel[0], F2=pixel[1], F3=pixel[2])
                if p in appearances:
                    appearances[p] += 1
                    appearances_as_skin[p] += 1
                else:
                    appearances[p] = 1
                    appearances_as_skin[p] = 1

    print("Calculating bayes spm components for nonskin images")
    non_skin_images = utils.load_images_from_folder(path_neg)
    for image in non_skin_images:
        image = utils.convert_color(image, color_space)

        rows = image.shape[0]
        cols = image.shape[1]
        for x_pixel in range(rows):
            for y_pixel in range(cols):
                non_skin_pixels += 1
                pixel = image[x_pixel, y_pixel]
                p = Pixel(F1=pixel[0], F2=pixel[1], F3=pixel[2])
                if p in appearances:
                    appearances[p] += 1
                else:
                    appearances[p] = 1

    return BayesSpmComponents(skin_pixels, non_skin_pixels, appearances, appearances_as_skin)


def __calculate_pixel_probability(pixel, bayes_spm_components):
    """
    Calculates the probability that the given pixel is a skin pixel

    uses the formula p = P(X|S) * P(S) / P(X)
    where S represents the prob of a pixel being a skin pixel ; X the probability of getting the selected pixel
    and P(X|S) the prob of finding this pixel given skin

    :param pixel:
    :param bayes_spm_components:
    :return:
    """
    p = Pixel(F1=pixel[0], F2=pixel[1], F3=pixel[2])

    if p not in bayes_spm_components.appearances_as_skin:
        return 0

    px = bayes_spm_components.appearances[p] / (bayes_spm_components.skin_pixels + bayes_spm_components.non_skin_pixels)
    ps = bayes_spm_components.skin_pixels / (bayes_spm_components.skin_pixels + bayes_spm_components.non_skin_pixels)
    pxs = bayes_spm_components.appearances_as_skin[p] / bayes_spm_components.skin_pixels
    return (pxs * ps) / px


"""
Global variable ; map that caches pixel probabilities when calculating spm as needed for input
"""
pixel_probability_cache = {}


def __calculate_pixel_probability_with_neighbours(pixel, bayes_spm_components, neighbour_area):
    """
    Calculates the probability of a pixel being a skin pixel by getting the max probability from its neighbours

    This is an optimisation trying to improve the aspect of having a lot of pixels not appearing in test data
    For each pixel we get the max probability of its neighbours withing the area in the RGB space

    :param pixel:
    :param bayes_spm_components:
    :return:
    """
    max_prob = 0
    area = neighbour_area
    for r_offset in range(-area, area, 1):
        for g_offset in range(-area, area, 1):
            for b_offset in range(-area, area, 1):
                p = [pixel[0] + r_offset, pixel[1] + g_offset, pixel[2] + b_offset]
                prob = __calculate_pixel_probability(p, bayes_spm_components)
                if prob > max_prob:
                    max_prob = prob
    return max_prob
