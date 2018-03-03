import cv2
import numpy as np


def combine_res(image, spm_img, texture_img):
    new_image = image.copy()
    new_image[:] = (255, 255, 255)  # make image white
    cv2.addWeighted(image, 0.4, new_image, 1 - 0.4, 0, new_image)  # overlay transparent img

    rows = image.shape[0]
    cols = image.shape[1]
    for x_pixel in range(rows):
        for y_pixel in range(cols):
            if np.all(spm_img[x_pixel, y_pixel] == 0) and np.all(texture_img[x_pixel, y_pixel] == 0):
                new_image[x_pixel, y_pixel] = [0, 0, 0]
    return new_image

'''
color = cv2.imread('color.png')
texture = cv2.imread('texture.png')
orig = cv2.imread('orig.jpg')

res = combine_res(orig, color, texture)
cv2.imwrite('res.png', res)
'''