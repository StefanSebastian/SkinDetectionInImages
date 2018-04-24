import numpy as np

from color_analysis.train.components import BayesSpmComponents
from utils import general
from utils.log import LogFactory
from utils.tuples import Pixel


class CompaqComponentExtractor:
    def __init__(self, path_train, color_space, logger=LogFactory.get_default_logger()):
        self.path_train = path_train
        self.color_space = color_space

        self.appearances = {}
        self.appearances_as_skin = {}
        self.skin_pixels = 0
        self.non_skin_pixels = 0

        self.logger = logger

    def extract_components(self):
        self.__compute_components()
        return BayesSpmComponents(self.skin_pixels, self.non_skin_pixels, self.appearances, self.appearances_as_skin)

    def __compute_components(self):
        try:
            self.__compute_components_for_positive_images()
            self.__compute_components_for_negative_images()
        except FileNotFoundError as e:
            self.logger.log("Error " + "invalid train path")
            raise e

    def __compute_components_for_positive_images(self):
        self.logger.log("Loading positive images")

        images = general.load_images_from_folder(self.path_train + "/" + "train_images")
        masks = general.load_images_from_folder(self.path_train + "/" + "train_masks")

        self.logger.log("\nExtracting values from positive images")
        for current_index in range(len(images)):
            self.logger.log_progress(current_index, len(images))
            image = images[current_index]
            mask = masks[current_index]

            image = general.convert_color(image, self.color_space)
            try:
                self.__get_components_from_image_mask(image, mask)
            except IndexError:
                self.logger.log(str(current_index) + " mask is corrupted")

    def __compute_components_for_negative_images(self):
        self.logger.log("Loading negative images")
        images = general.load_images_from_folder(self.path_train + "/" + "train_images_ns")

        self.logger.log("\nExtracting values from negative images")
        for current_index in range(len(images)):
            self.logger.log_progress(current_index, len(images))
            image = images[current_index]

            image = general.convert_color(image, self.color_space)
            mask = np.zeros(image.shape)
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
