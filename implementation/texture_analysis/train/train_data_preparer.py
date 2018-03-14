from utils import utils
import cv2
import numpy as np


class TrainDataPreparer:
    def __init__(self, path_pos, path_neg, skin_label, non_skin_label, feature_extractor):
        self.path_pos = path_pos
        self.path_neg = path_neg
        self.skin_label = skin_label
        self.non_skin_label = non_skin_label
        self.feature_extractor = feature_extractor

    def get_train_data(self):
        """
        Get training data for texture detection
        """
        print("Extracting features from training data")

        features = []
        labels = []

        print("Positive images: ")
        progress = 0

        skin_images = utils.load_images_from_folder(self.path_pos)
        for image in skin_images:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            features.append(self.feature_extractor.extract(gray))
            labels.append(self.skin_label)

            progress += 1
            utils.print_progress(progress, len(skin_images))

        print("\nNegative images: ")
        progress = 0

        non_skin_images = utils.load_images_from_folder(self.path_neg)
        for image in non_skin_images:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            features.append(self.feature_extractor.extract(gray))
            labels.append(self.non_skin_label)

            progress += 1
            utils.print_progress(progress, len(non_skin_images))

        print("\nTraining features: {}".format(np.array(features).shape))
        print("Training labels: {}".format(np.array(labels).shape))
        return features, labels
