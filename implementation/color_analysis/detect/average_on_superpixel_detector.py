from utils import utils
from color_analysis.detect.utils import calculate_pixel_probability


class AverageOnSuperpixelDetector:
    def __init__(self, model):
        self.model = model

    def detect(self, image, superpixels, threshold):
        new_image = utils.generate_overlay_image(image)
        image = utils.convert_color(image, self.model.color_space)

        pos = 0
        for center in superpixels:  # iterate superpixels
            pos += 1
            utils.print_progress(pos, len(superpixels))

            superpixel = superpixels[center]
            total_prob = 0
            count = 0
            for pixel_pos in superpixel.get_pixels_pos(): # iterate all pixels in superpixel
                x_pixel, y_pixel = pixel_pos[0], pixel_pos[1]
                prob = calculate_pixel_probability(image[x_pixel, y_pixel], self.model.components)
                total_prob += prob
                count += 1

            # determine based on max probability if the region is classified as skin
            if (total_prob / count) > threshold:
                for pixel_pos in superpixel.get_pixels_pos():
                    x_pixel, y_pixel = pixel_pos[0], pixel_pos[1]
                    new_image[x_pixel, y_pixel] = [0, 0, 0]

        return new_image
