from utils import utils
from color_analysis.detect.utils import calculate_pixel_probability


class SimpleDetector:
    def __init__(self, model):
        self.model = model

    def detect(self, image, threshold):
        new_image = utils.generate_overlay_image(image)

        image = utils.convert_color(image, self.model.color_space)

        rows = image.shape[0]
        cols = image.shape[1]
        for x_pixel in range(rows):
            for y_pixel in range(cols):
                utils.print_progress_pixel(x_pixel, y_pixel, rows, cols)

                pixel = image[x_pixel, y_pixel]
                prob = calculate_pixel_probability(pixel, self.model.components)

                if prob > threshold:
                    new_image[x_pixel, y_pixel] = [0, 0, 0]
        return new_image


