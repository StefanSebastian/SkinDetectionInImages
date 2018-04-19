from color_analysis.train.components import BayesSpmComponents
from utils import general
from utils.log import LogFactory
from utils.tuples import Pixel


class SfaComponentExtractor:
    def __init__(self, path_positive_images, path_negative_images, color_space, logger=LogFactory.get_default_logger()):
        self.path_positive_images = path_positive_images
        self.path_negative_images = path_negative_images
        self.color_space = color_space

        self.appearances = {}
        self.appearances_as_skin = {}
        self.skin_pixels = 0
        self.non_skin_pixels = 0

        self.logger = logger

    def extract_components(self):
        self.extract_skin_pixels()
        self.extract_non_skin_pixels()
        return BayesSpmComponents(self.skin_pixels, self.non_skin_pixels, self.appearances, self.appearances_as_skin)

    def extract_skin_pixels(self):
        self.logger.log("Calculating bayes spm components for skin images")
        skin_images = general.load_images_from_folder(self.path_positive_images)
        for image in skin_images:
            image = general.convert_color(image, self.color_space)

            rows = image.shape[0]
            cols = image.shape[1]
            for x_pixel in range(rows):
                for y_pixel in range(cols):
                    self.skin_pixels += 1
                    pixel = image[x_pixel, y_pixel]
                    p = Pixel(F1=pixel[0], F2=pixel[1], F3=pixel[2])
                    if p in self.appearances:
                        self.appearances[p] += 1
                        self.appearances_as_skin[p] += 1
                    else:
                        self.appearances[p] = 1
                        self.appearances_as_skin[p] = 1

    def extract_non_skin_pixels(self):
        self.logger.log("Calculating bayes spm components for nonskin images")
        non_skin_images = general.load_images_from_folder(self.path_negative_images)
        for image in non_skin_images:
            image = general.convert_color(image, self.color_space)

            rows = image.shape[0]
            cols = image.shape[1]
            for x_pixel in range(rows):
                for y_pixel in range(cols):
                    self.non_skin_pixels += 1
                    pixel = image[x_pixel, y_pixel]
                    p = Pixel(F1=pixel[0], F2=pixel[1], F3=pixel[2])
                    if p in self.appearances:
                        self.appearances[p] += 1
                    else:
                        self.appearances[p] = 1
