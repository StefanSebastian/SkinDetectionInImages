import numpy as np


class Stats:
    def __init__(self,
                 image_index,
                 true_positive_rate,
                 false_positive_rate,
                 true_negative_rate,
                 false_negative_rate,
                 accuracy,
                 precision,
                 recall):
        self.image_index = image_index
        self.false_negative_rate = false_negative_rate
        self.true_negative_rate = true_negative_rate
        self.false_positive_rate = false_positive_rate
        self.true_positive_rate = true_positive_rate
        self.recall = recall
        self.precision = precision
        self.accuracy = accuracy

    def __str__(self):
        res = 'image_index: ' + str(self.image_index) + '\n'
        res += 'true_positive_rate: ' + str(self.true_positive_rate) + '\n'
        res += 'false_positive_rate: ' + str(self.false_positive_rate) + '\n'
        res += 'true_negative_rate: ' + str(self.true_negative_rate) + '\n'
        res += 'false_negative_rate: ' + str(self.false_negative_rate) + '\n'
        res += 'accuracy: ' + str(self.accuracy) + '\n'
        res += 'precision: ' + str(self.precision) + '\n'
        res += 'recall: ' + str(self.recall) + '\n'
        return res

    @staticmethod
    def get_csv_header():
        header = "image_index,true_positive_rate,false_positive_rate,"
        header += "true_negative_rate,false_negative_rate,"
        header += "accuracy,precision,recall"
        return header

    def get_as_csv(self):
        res = str(self.image_index) + ","
        res += str(self.true_positive_rate) + ","
        res += str(self.false_positive_rate) + ","
        res += str(self.true_negative_rate) + ","
        res += str(self.false_negative_rate) + ","
        res += str(self.accuracy) + ","
        res += str(self.precision) + ","
        res += str(self.recall) + '\n'
        return res


def get_stats(expected_image, actual_image, image_index):
    """
    Using data from SFA database
    by convention the expected image has every non-skin pixel set in black

    actual_image has every predicted skin pixel set in black
    :param expected_image:
    :param actual_image:
    :return:
    """
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    rows = actual_image.shape[0]
    cols = actual_image.shape[1]

    total_pixels = rows * cols

    for x_pixel in range(rows):
        for y_pixel in range(cols):
            if np.all(actual_image[x_pixel, y_pixel] == 0) and not np.all(expected_image[x_pixel, y_pixel] == 0):
                true_positive += 1
            if np.all(actual_image[x_pixel, y_pixel] == 0) and np.all(expected_image[x_pixel, y_pixel] == 0):
                false_positive += 1
            if not np.all(actual_image[x_pixel, y_pixel] == 0) and np.all(expected_image[x_pixel, y_pixel] == 0):
                true_negative += 1
            if not np.all(actual_image[x_pixel, y_pixel] == 0) and not np.all(expected_image[x_pixel, y_pixel] == 0):
                false_negative += 1

    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_negative + false_negative)

    true_positive_rate = true_positive / (true_positive + false_negative)
    false_positive_rate = false_positive / (false_positive + true_negative)
    true_negative_rate = true_negative / (true_negative + false_positive)
    false_negative_rate = false_negative / (false_negative + true_positive)

    return Stats(image_index,
                 true_positive_rate,
                 false_positive_rate,
                 true_negative_rate,
                 false_negative_rate,
                 accuracy,
                 precision,
                 recall)
