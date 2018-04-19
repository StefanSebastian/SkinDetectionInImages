from color_analysis.detect.calculate.calculate_probability import ProbabilityCalculator
from utils import general
from utils.log import LogFactory


class SimpleDetector:
    def __init__(self, model, logger=LogFactory.get_default_logger()):
        self.model = model
        self.logger = logger

    def detect(self, image, threshold):
        new_image = general.generate_overlay_image(image)

        image = general.convert_color(image, self.model.color_space)

        rows = image.shape[0]
        cols = image.shape[1]
        for x_pixel in range(rows):
            for y_pixel in range(cols):
                self.logger.print_progress_pixel(x_pixel, y_pixel, rows, cols)

                pixel = image[x_pixel, y_pixel]
                prob = ProbabilityCalculator.calculate_for_pixel(pixel, self.model.components)

                if prob > threshold:
                    new_image[x_pixel, y_pixel] = [0, 0, 0]
        return new_image


