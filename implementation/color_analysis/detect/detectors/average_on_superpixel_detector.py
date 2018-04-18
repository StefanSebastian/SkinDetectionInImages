from color_analysis.detect.calculate.cached_probability_calculator import CachedProbabilityCalculator
from utils import utils


class AverageOnSuperpixelDetector:
    def __init__(self, model, window_size):
        self.model = model
        self.window_size = window_size
        self.probability_calculator = CachedProbabilityCalculator()

    def detect(self, image, superpixels, threshold):
        new_image = utils.generate_overlay_image(image)
        image = utils.convert_color(image, self.model.color_space)

        pos = 0
        for center in superpixels:  # iterate superpixels
            pos += 1
            utils.print_progress(pos, len(superpixels))

            superpixel = superpixels[center]
            average_prob = self.__calculate_superpixel_average(superpixel, image)

            # determine based on max probability if the region is classified as skin
            if average_prob > threshold:
                for pixel_pos in superpixel.get_pixels_pos():
                    x_pixel, y_pixel = pixel_pos[0], pixel_pos[1]
                    new_image[x_pixel, y_pixel] = [0, 0, 0]

        return new_image

    def __calculate_superpixel_average(self, superpixel, image):
        """
        Gets the average skin probability of a superpixel
        """
        total_prob = 0
        count = 0
        for pixel_pos in superpixel.get_pixels_pos():  # iterate all pixels in superpixel
            considered_pixel = image[pixel_pos[0], pixel_pos[1]]

            prob = self.probability_calculator.calculate_pixel_probability(
                considered_pixel, self.model.components, self.window_size)

            total_prob += prob
            count += 1
        return total_prob / count



