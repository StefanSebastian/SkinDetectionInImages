from skin_probability_map.bayes.train.components import BayesSpmComponents
from utils import utils
from utils.utils import Pixel

import numpy as np


class CompaqComponentExtractor:
    def __init__(self, path_train, color_space):
        self.path_train = path_train
        self.color_space = color_space

        self.appearances = {}
        self.appearances_as_skin = {}
        self.skin_pixels = 0
        self.non_skin_pixels = 0

    def extract_components(self):
        self.__compute_components()
        return BayesSpmComponents(self.skin_pixels, self.non_skin_pixels, self.appearances, self.appearances_as_skin)

    def __compute_components(self):
        images = utils.load_images_from_folder(self.path_train + "/" + "train_images")
        masks = utils.load_images_from_folder(self.path_train + "/" + "train_masks")

        for current_index in range(len(images)):
            utils.print_progress(current_index, len(images))
            image = images[current_index]
            mask = masks[current_index]

            image = utils.convert_color(image, self.color_space)

            self.__get_components_from_image_mask(image, mask)

    def __get_components_from_image_mask(self, image, mask):
        """
        Extracts bayes components from an image given a mask
        """
        rows = image.shape[0]
        cols = image.shape[1]
        for x_pixel in range(rows):
            for y_pixel in range(cols):
                pixel = image[x_pixel, y_pixel]
                p = Pixel(F1=pixel[0], F2=pixel[1], F3=pixel[2])
                if np.all(mask[x_pixel, y_pixel] == 0):  # not skin
                    self.non_skin_pixels += 1
                    if p in self.appearances:
                        self.appearances[p] += 1
                    else:
                        self.appearances[p] = 1
                else:
                    self.skin_pixels += 1

                    if p in self.appearances:
                        self.appearances[p] += 1
                    else:
                        self.appearances[p] = 1

                    if p in self.appearances_as_skin:
                        self.appearances_as_skin[p] += 1
                    else:
                        self.appearances_as_skin[p] = 1
