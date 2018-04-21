import cv2
import numpy as np

from utils import general
from utils.log import LogFactory


class PerPixelDetector:
    def __init__(self, model, grid_size, logger=LogFactory.get_default_logger()):
        self.model = model
        self.grid_size = grid_size
        self.logger = logger

    def detect(self, image):
        """
        Gets the image skin region by building a window around each pixel.
        Result is smooth but processing time is increased.
        """
        return self.__detect_template(image)

    def detect_with_mask(self, image, mask):
        """
        Gets the image skin region by building a window around each pixel.
        Uses mask to only consider pixels that have been marked.
        """
        def mask_filter(x, y): return np.all(mask[x, y] == 0)
        return self.__detect_template(image, mask_filter)

    def __detect_template(self, image, mask=lambda x, y: True):
        new_image = general.generate_overlay_image(image)

        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        rows = gray.shape[0]
        cols = gray.shape[1]

        radius = self.grid_size // 2
        for x_pixel in range(radius, rows - radius):
            for y_pixel in range(radius, cols - radius):
                self.logger.print_progress_pixel(x_pixel, y_pixel, rows, cols)

                if mask(x_pixel, y_pixel):
                    r = x_pixel - radius
                    c = y_pixel - radius
                    grid_size = self.grid_size
                    roi = gray[r:r + grid_size, c:c + grid_size]

                    prediction = self.model.classify(roi)
                    if prediction == self.model.skin_label:
                        new_image[x_pixel, y_pixel] = [0, 0, 0]
        return new_image
