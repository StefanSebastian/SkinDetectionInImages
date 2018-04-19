import os
import cv2
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
    if progress % 300 == 0:  # to avoid too many writes
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


def convert_color(image, color_space):
    """
    Convert RGB image to the given colorspace

    :param image:
    :param color_space:
    :return:
    """
    if color_space == 'HSV':
        return cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    elif color_space == 'YCrCb':
        return cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
    elif color_space == 'RGB':
        return image


def generate_overlay_image(image):
    new_image = image.copy()
    new_image[:] = (255, 255, 255)  # make image white
    cv2.addWeighted(image, 0.4, new_image, 1 - 0.4, 0, new_image)  # overlay transparent img
    return new_image


def safe_div(x, y):
    if y == 0:
        return 0
    else:
        return x / y
