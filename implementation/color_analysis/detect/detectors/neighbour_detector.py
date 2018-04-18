from color_analysis.detect.calculate.cached_probability_calculator import CachedProbabilityCalculator
from utils import utils


class NeighbourDetector:
    """
    Calculates pixel probability by considering its neighbours
    """

    def __init__(self, model, neighbour_area):
        self.model = model
        self.neighbour_area = neighbour_area
        self.probability_calculator = CachedProbabilityCalculator()

    def detect(self, image, threshold):
        new_image = utils.generate_overlay_image(image)
        image = utils.convert_color(image, self.model.color_space)

        rows = image.shape[0]
        cols = image.shape[1]
        for x_pixel in range(rows):
            for y_pixel in range(cols):
                utils.print_progress_pixel(x_pixel, y_pixel, rows, cols)

                pixel = image[x_pixel, y_pixel]

                prob = self.probability_calculator.calculate_pixel_probability(
                    pixel, self.model.components, self.neighbour_area)

                if prob > threshold:
                    new_image[x_pixel, y_pixel] = [0, 0, 0]
        return new_image

