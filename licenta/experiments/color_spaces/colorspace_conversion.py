import cv2


def convert(image, colorspace):
    """
    Convert RGB image to the given colorspace

    :param image:
    :param colorspace:
    :return:
    """
    if colorspace == 'HSV':
        return cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    elif colorspace == 'YCrCb':
        return cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
    elif colorspace == 'RGB':
        return image
