from utils import utils
from utils.tuples import Pixel
from color_analysis.detect.utils import calculate_pixel_probability


class NeighbourDetector:
    def __init__(self, model, neighbour_area):
        self.model = model
        self.neighbour_area = neighbour_area
        self.pixel_probability_cache = {}

    def detect(self, image, threshold):
        new_image = utils.generate_overlay_image(image)

        image = utils.convert_color(image, self.model.color_space)

        rows = image.shape[0]
        cols = image.shape[1]
        for x_pixel in range(rows):
            for y_pixel in range(cols):
                utils.print_progress_pixel(x_pixel, y_pixel, rows, cols)

                pixel = image[x_pixel, y_pixel]

                # check cache
                p = Pixel(F1=pixel[0], F2=pixel[1], F3=pixel[2])
                if p in self.pixel_probability_cache:
                    prob = self.pixel_probability_cache[p]
                else:
                    prob = self.__calculate_pixel_probability_with_neighbours(pixel)
                    self.pixel_probability_cache[p] = prob

                if prob > threshold:
                    new_image[x_pixel, y_pixel] = [0, 0, 0]
        return new_image

    def __calculate_pixel_probability_with_neighbours(self, pixel):
        max_prob = 0
        area = self.neighbour_area
        for r_offset in range(-area, area, 1):
            for g_offset in range(-area, area, 1):
                for b_offset in range(-area, area, 1):
                    p = [pixel[0] + r_offset, pixel[1] + g_offset, pixel[2] + b_offset]
                    prob = calculate_pixel_probability(p, self.model.components)
                    if prob > max_prob:
                        max_prob = prob
        return max_prob
