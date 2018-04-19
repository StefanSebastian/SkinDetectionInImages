import numpy as np

from utils import general


class Combiner:
    @staticmethod
    def combine_res(image, spm_img, texture_img):
        new_image = general.generate_overlay_image(image)

        rows = image.shape[0]
        cols = image.shape[1]
        for x_pixel in range(rows):
            for y_pixel in range(cols):
                if np.all(spm_img[x_pixel, y_pixel] == 0) and np.all(texture_img[x_pixel, y_pixel] == 0):
                    new_image[x_pixel, y_pixel] = [0, 0, 0]
        return new_image
