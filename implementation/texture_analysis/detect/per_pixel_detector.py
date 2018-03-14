from utils import utils

import cv2


class PerPixelDetector:
    def __init__(self, model, radius):
        self.model = model
        self.radius = radius

    def detect(self, image):
        """
            Gets the image skin region by building a window around each pixel

            Result is smooth but processing time is increased

            :param classifier:
            :param image:
            :param radius:
            :return:
            """
        new_image = utils.generate_overlay_image(image)

        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        rows = gray.shape[0]
        cols = gray.shape[1]

        radius = self.radius
        for x_pixel in range(radius, rows - radius):
            for y_pixel in range(radius, cols - radius):
                utils.print_progress_pixel(x_pixel, y_pixel, rows, cols)

                r = x_pixel - radius
                c = y_pixel - radius
                grid_size = 2 * radius
                roi = gray[r:r + grid_size, c:c + grid_size]

                prediction = self.model.classify(roi)
                if prediction == self.model.skin_label:
                    new_image[x_pixel, y_pixel] = [0, 0, 0]
        return new_image
