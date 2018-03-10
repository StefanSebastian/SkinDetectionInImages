from utils.utils import distance2d
from utils.utils import Pixel
import operator

class Superpixel:
    def __init__(self, root_pixel_pos, image):
        self.image = image
        self.root_pixel_pos = root_pixel_pos
        self.pixels_pos = []
        self.features = None

    def add_pixel(self, pixel_pos):
        self.pixels_pos.append(pixel_pos)

    def set_features(self, features):
        self.features = features

    def get_root_pixel_pos(self):
        return self.root_pixel_pos

    def get_pixels_pos(self):
        return self.pixels_pos

    def get_image(self):
        return self.image

    def __key(self):
        return self.root_pixel_pos

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return str(self.root_pixel_pos) + ' ' + str(self.pixels_pos)

    def __repr__(self):
        repres = "Superpixel : {\n"
        repres += "Root pixel " + str(self.root_pixel_pos) + "\n"
        repres += "Component pixels " + str(self.pixels_pos) + "\n"
        repres += "Features " + str(self.features) + "\n"
        repres += "}"
        return repres


class SuperpixelFeatures:
    def __init__(self, r_min_pos, r_max_pos, g_min_pos, g_max_pos, b_min_pos, b_max_pos,
                 least_freq_color, most_freq_color):
        self.b_max_pos = b_max_pos
        self.b_min_pos = b_min_pos
        self.g_max_pos = g_max_pos
        self.g_min_pos = g_min_pos
        self.r_max_pos = r_max_pos
        self.r_min_pos = r_min_pos

        self.a = distance2d(r_min_pos, r_max_pos) / 2
        self.b = distance2d(g_min_pos, g_max_pos) / 2
        self.c = distance2d(r_min_pos, r_max_pos) / 2

        self.most_freq_color = most_freq_color
        self.least_freq_color = least_freq_color

    def __repr__(self):
        repres = "\n{\n"
        repres += "R min pos : " + str(self.r_min_pos) + "\n"
        repres += "R max pos : " + str(self.r_max_pos) + "\n"
        repres += "G min pos : " + str(self.g_min_pos) + "\n"
        repres += "G max pos : " + str(self.g_max_pos) + "\n"
        repres += "B min pos : " + str(self.b_min_pos) + "\n"
        repres += "B max pos : " + str(self.b_max_pos) + "\n"
        repres += "a : " + str(self.a) + "\n"
        repres += "b : " + str(self.b) + "\n"
        repres += "c : " + str(self.c) + "\n"
        repres += "least freq color : " + str(self.least_freq_color) + "\n"
        repres += "most freq color : " + str(self.most_freq_color) + "\n"
        repres += "}\n"
        return repres

    @staticmethod
    def calculate_features(superpixel):
        pixels_pos = superpixel.get_pixels_pos()
        image = superpixel.get_image()

        pixel_frequencies = {}
        min_r, min_g, min_b, max_r, max_g, max_b = 256, 256, 256, -1, -1, -1
        r_min_pos, r_max_pos, g_min_pos, g_max_pos, b_min_pos, b_max_pos = \
            [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1]
        for pixel_pos in pixels_pos:
            pixel = image[pixel_pos[0], pixel_pos[1]]
            # R
            if pixel[0] < min_r:
                r_min_pos = pixel_pos
                min_r = pixel[0]
            if pixel[0] > max_r:
                r_max_pos = pixel_pos
                max_r = pixel[0]
            # G
            if pixel[1] < min_g:
                g_min_pos = pixel_pos
                min_g = pixel[1]
            if pixel[1] > max_g:
                g_max_pos = pixel_pos
                max_g = pixel[1]
            # B
            if pixel[2] < min_b:
                b_min_pos = pixel_pos
                min_b = pixel[2]
            if pixel[2] > max_b:
                b_max_pos = pixel_pos
                max_b = pixel[2]

            pixel_tuple = Pixel(R=pixel[0], G=pixel[1], B=pixel[2])
            if pixel_tuple in pixel_frequencies:
                pixel_frequencies[pixel_tuple] += 1
            else:
                pixel_frequencies[pixel_tuple] = 1

        sorted_pixels = sorted(pixel_frequencies.items(), key=operator.itemgetter(1))
        least_freq_pixel = sorted_pixels[0][0]
        least_frequent_color = [least_freq_pixel.R, least_freq_pixel.G, least_freq_pixel.B]
        most_freq_pixel = sorted_pixels[len(sorted_pixels) - 1][0]
        most_frequent_color = [most_freq_pixel.R, most_freq_pixel.G, most_freq_pixel.B]

        return SuperpixelFeatures(r_min_pos, r_max_pos, g_min_pos, g_max_pos, b_min_pos, b_max_pos,
                                  least_frequent_color, most_frequent_color)
