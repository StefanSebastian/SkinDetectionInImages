import numpy as np
import random
import cv2


def fill_contours_with_random_colors(image, contours):
    new_im = np.zeros(image.shape)

    for i in range(len(contours)):
        contour = contours[i]
        if contour.shape[0] < 3:
            continue

        # get frame
        x_upper = -1
        y_upper = -1
        x_lower = -1
        y_lower = -1
        for j in range(contour.shape[0]):
            point = contour[j][0]
            x_aux = point[0]
            y_aux = point[1]
            point[0] = y_aux
            point[1] = x_aux

            if point[0] < x_upper or x_upper == -1:
                x_upper = point[0]
            if point[1] < y_upper or y_upper == -1:
                y_upper = point[1]
            if point[0] > x_lower or x_lower == -1:
                x_lower = point[0]
            if point[1] > y_lower or y_lower == -1:
                y_lower = point[1]

        color_for_contour = np.array(
            [int(random.random() * 256), int(random.random() * 256), int(random.random() * 256)])
        for x_pixel in range(x_upper, x_lower + 1):
            for y_pixel in range(y_upper, y_lower + 1):
                if 0 <= x_pixel < image.shape[0] and 0 <= y_pixel < image.shape[1]:
                    if cv2.pointPolygonTest(contour, (x_pixel, y_pixel), True) > 0:
                        new_im[x_pixel, y_pixel] = color_for_contour
    return new_im


def fill_contours_with_super_pixels(image, contours, super_pixels):
    new_im = np.zeros(image.shape)

    for i in range(len(contours)):
        contour = contours[i]
        if contour.shape[0] < 3:
            continue

        # get frame
        x_upper = -1
        y_upper = -1
        x_lower = -1
        y_lower = -1
        for j in range(contour.shape[0]):
            point = contour[j][0]
            x_aux = point[0]
            y_aux = point[1]
            point[0] = y_aux
            point[1] = x_aux

            if point[0] < x_upper or x_upper == -1:
                x_upper = point[0]
            if point[1] < y_upper or y_upper == -1:
                y_upper = point[1]
            if point[0] > x_lower or x_lower == -1:
                x_lower = point[0]
            if point[1] > y_lower or y_lower == -1:
                y_lower = point[1]

        for x_pixel in range(x_upper, x_lower + 1):
            for y_pixel in range(y_upper, y_lower + 1):
                if 0 <= x_pixel < image.shape[0] and 0 <= y_pixel < image.shape[1]:
                    if cv2.pointPolygonTest(contour, (x_pixel, y_pixel), True) > 0:
                        new_im[x_pixel, y_pixel] = super_pixels[x_pixel, y_pixel]
    return new_im
