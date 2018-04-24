from color_analysis.detect.calculate.cached_probability_calculator import CachedProbabilityCalculator
from utils import general
from utils.log import LogFactory


class NeighbourDetector:
    """
    Calculates pixel probability by considering its neighbours
    """

    def __init__(self, model, neighbour_area, logger=LogFactory.get_default_logger()):
        self.model = model
        self.neighbour_area = neighbour_area
        self.probability_calculator = CachedProbabilityCalculator()
        self.logger = logger

    def detect(self, image, threshold):
        new_image = general.generate_overlay_image(image)
        image = general.convert_color(image, self.model.color_space)

        rows = image.shape[0]
        cols = image.shape[1]
        for x_pixel in range(rows):
            for y_pixel in range(cols):
                self.logger.log_progress_pixel(x_pixel, y_pixel, rows, cols)

                pixel = image[x_pixel, y_pixel]

                prob = self.probability_calculator.calculate_pixel_probability(
                    pixel, self.model.components, self.neighbour_area)

                if prob > threshold:
                    new_image[x_pixel, y_pixel] = [0, 0, 0]
        return new_image

