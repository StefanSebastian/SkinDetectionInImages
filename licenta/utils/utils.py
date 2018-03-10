import os
import cv2
from collections import namedtuple
from math import sqrt


def print_progress(pos, total):
    """
    Utility method to print the progress of an operation

    :param pos:
    :param total:
    :return:
    """
    progress = pos / total
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50), progress * 100), end="", flush=True)


def print_progress_pixel(x_pixel, y_pixel, rows, cols):
    """
    Prints the progress of the current pixel operation
    determines the location of the pixel out of the total pixels

    :param x_pixel: row of pixel
    :param y_pixel: col of pixel
    :param rows: nr rows of image
    :param cols: nr cols of image
    :return:
    """
    progress = x_pixel * cols + y_pixel
    progress = progress / (rows * cols)
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50), progress * 100), end="", flush=True)


def load_images_from_folder(folder):
    """
    Utility method that loads all images from a folder

    :param folder:
    :return:
    """
    images = []
    for filename in os.listdir(folder):
        print("reading " + filename)
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
        print("Images read " + str(len(images)))
    return images


def image_chopper(input_path, result_path, grid_size):
    image_index = 0
    images = load_images_from_folder(input_path)
    for image in images:
        image_index += 1
        print("Image : " + str(image_index))
        chop(image, grid_size, image_index, result_path)


def chop(image, grid_size, image_index, result_path):
    rows = image.shape[0]
    cols = image.shape[1]
    grid_position = 0
    for r in range(0, rows - grid_size, grid_size):
        for c in range(0, cols - grid_size, grid_size):
            print_progress_pixel(r, c, rows, cols)
            grid_position += 1
            roi = image[r:r + grid_size, c:c + grid_size]
            cv2.imwrite(result_path + "/" + str(image_index) + "-" + str(grid_position) + ".png", roi)


def filter_corrupt_data(input_path, mask_path, output_image_path, output_mask_path):
    """
    Used to filter corrupt images from compaq

    :param input_path:
    :param mask_path:
    :param output_image_path:
    :param output_mask_path:
    :return:
    """
    for image_name in os.listdir(input_path):
        print("reading " + image_name)
        img = cv2.imread(os.path.join(input_path, image_name))

        if img is not None:
            search_mask = image_name.split(".")[0] + ".pbm"
            for mask_name in os.listdir(mask_path):
                if mask_name == search_mask:
                    mask = cv2.imread(os.path.join(mask_path, mask_name))
                    if mask is not None:
                        cv2.imwrite(output_image_path + "/" + image_name.split(".")[0] + ".png", img)
                        cv2.imwrite(output_mask_path + "/" + mask_name, mask)


def distance2d(p1, p2):
    x1, x2, y1, y2 = p1[0], p2[0], p1[1], p2[1]
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

"""
Tuple for position
"""
Position = namedtuple("Position", ["X", "Y"])

"""
Named tuple representing a pixel
"""
Pixel = namedtuple("Pixel", ["R", "G", "B"])