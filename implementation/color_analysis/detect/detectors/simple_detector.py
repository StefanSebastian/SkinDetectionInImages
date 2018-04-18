from color_analysis.detect.calculate.calculate_probability import ProbabilityCalculator
from utils import utils


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
                prob = ProbabilityCalculator.calculate_for_pixel(pixel, self.model.components)

                if prob > threshold:
                    new_image[x_pixel, y_pixel] = [0, 0, 0]
        return new_image


