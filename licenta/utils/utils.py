import os
import cv2


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
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images
