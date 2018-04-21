import mahotas as mt
from sklearn.externals import joblib

from texture_analysis.train.model import TextureModel
from texture_analysis.train.svm_classifier import SvmClassifier
from texture_analysis.train.train_data_preparer import TrainDataPreparer
from utils.log import LogFactory
from utils.serialization import SerializationUtils


class HaralickModelTrainer:
    def __init__(self, path_pos, path_neg, skin_label, non_skin_label, logger=LogFactory.get_default_logger()):
        self.path_pos = path_pos
        self.path_neg = path_neg
        self.skin_label = skin_label
        self.non_skin_label = non_skin_label
        self.model = None
        self.logger = logger

    def train_and_store_model(self, model_path):
        self.logger.log("Extracting haralick features")
        feature_extractor = HaralickFeatureExtractor()

        self.logger.log("Preparing train data")
        data_prepare = TrainDataPreparer(
            self.path_pos, self.path_neg, self.skin_label, self.non_skin_label, feature_extractor, self.logger)
        features, labels = data_prepare.get_train_data()

        self.logger.log("Training svm classifier")
        svm_classifier = SvmClassifier.train_svm_classifier(features, labels)
        self.model = HaralickModel(feature_extractor, svm_classifier, self.skin_label)
        self.__store_model(model_path)

    def __store_model(self, model_path):
        self.logger.log("Storing svm model")
        serializator = SerializationUtils()
        serializator.store_joblib_object(self.model, model_path)


class HaralickFeatureExtractor:
    def extract(self, image):
        """
        Extracts haralick features from a given image
        """
        textures = mt.features.haralick(image)
        ht_mean = textures.mean(axis=0)
        return ht_mean


class HaralickModel(TextureModel):
    def classify(self, image):
        features = self.feature_extractor.extract(image)
        return self.classifier.predict(features.reshape(1, -1))[0]
