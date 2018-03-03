import cv2
import mahotas as mt
import numpy as np
from sklearn.externals import joblib
from sklearn.svm import LinearSVC

from texture_detection import config
from utils import utils, serialization


def train_model():
    """
    Gets examples path from config, trains a svm then dumps the model in a file
    :return:
    """
    features, labels = __get_train_data(config.path_pos, config.path_neg)
    svm_classifier = __train_svm_classifier(features, labels)
    # save to file
    joblib.dump(svm_classifier, config.path_models + '/svm_classifier.pkl')

    return svm_classifier


def detect_skin_texture_default(image):
    """
    Applies skin detection with parameters from config file

    :param image:
    :return:
    """
    classifier = serialization.load_object(config.path_models + '/' + config.selected_classifier)
    if config.detection_type == 0:
        return get_image_skin_regions_by_grid(classifier, image, config.detection_window_size)
    else:
        return get_image_skin_regions_by_pixels(classifier, image, config.detection_window_size)


def get_image_skin_regions_by_grid(classifier, image, grid_size):
    """
    Gets the skin regions from an image by iterating with a window over the original image

    The resulting image has rough edges but the computation time is faster than the alternatives

    :param classifier:
    :param image:
    :param grid_size:
    :return:
    """
    new_image = image.copy()
    new_image[:] = (255, 255, 255)  # make image white
    cv2.addWeighted(image, 0.4, new_image, 1 - 0.4, 0, new_image)  # overlay transparent img

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    rows = gray.shape[0]
    cols = gray.shape[1]

    # cut image in little pieces
    for r in range(0, rows - grid_size, grid_size):
        for c in range(0, cols - grid_size, grid_size):
            utils.print_progress_pixel(r, c, rows, cols)
            roi = gray[r:r + grid_size, c:c + grid_size]
            feature = __extract_features(roi)
            prediction = classifier.predict(feature.reshape(1, -1))[0]
            if prediction == config.skin_label:
                cv2.rectangle(new_image, (c, r), (c + grid_size, r + grid_size), (0, 0, 0), -1)
    return new_image


def get_image_skin_regions_by_pixels(classifier, image, radius):
    """
    Gets the image skin region by building a window around each pixel

    Result is smooth but processing time is increased

    :param classifier:
    :param image:
    :param radius:
    :return:
    """
    new_image = image.copy()
    new_image[:] = (255, 255, 255)  # make image white
    cv2.addWeighted(image, 0.4, new_image, 1 - 0.4, 0, new_image)  # overlay transparent img

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    rows = gray.shape[0]
    cols = gray.shape[1]

    for x_pixel in range(radius, rows - radius):
        for y_pixel in range(radius, cols - radius):
            utils.print_progress_pixel(x_pixel, y_pixel, rows, cols)

            r = x_pixel - radius
            c = y_pixel - radius
            grid_size = 2 * radius
            roi = gray[r:r + grid_size, c:c + grid_size]
            feature = __extract_features(roi)
            prediction = classifier.predict(feature.reshape(1, -1))[0]
            if prediction == config.skin_label:
                new_image[x_pixel, y_pixel] = [0, 0, 0]
    return new_image


def __extract_features(image):
    """
    Extracts haralick features from a given image

    :param image:
    :return:
    """
    textures = mt.features.haralick(image)
    ht_mean = textures.mean(axis=0)
    return ht_mean


def __get_train_data(path_pos, path_neg):
    """
    Get training data for texture detection

    :param path_pos:
    :param path_neg:
    :return:
    """
    print("Extracting haralick features from training data")

    features = []
    labels = []

    print("Positive images: ")
    progress = 0

    skin_images = utils.load_images_from_folder(path_pos)
    for image in skin_images:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        features.append(__extract_features(gray))
        labels.append(config.skin_label)

        progress += 1
        utils.print_progress_pixel(progress, len(skin_images))

    print("\nNegative images: ")
    progress = 0

    non_skin_images = utils.load_images_from_folder(path_neg)
    for image in non_skin_images:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        features.append(__extract_features(gray))
        labels.append(config.non_skin_label)

        progress += 1
        utils.print_progress_pixel(progress, len(non_skin_images))

    print("\nTraining features: {}".format(np.array(features).shape))
    print("Training labels: {}".format(np.array(labels).shape))
    return features, labels


def __train_svm_classifier(features, labels):
    """
    Trains a svm classifier for the given features/labels

    :param features:
    :param labels:
    :return:
    """
    print("Creating the svm classifier")
    svm_classifier = LinearSVC(random_state=9)
    print("Training the classifier")
    svm_classifier.fit(features, labels)
    return svm_classifier

