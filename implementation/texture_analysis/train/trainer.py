from texture_analysis.train.haralick import HaralickModelTrainer
from texture_analysis.train.train_configuration import TextureTrainConfiguration
from utils.log import LogFactory


class TextureModelTrainer:
    def __init__(self, path_pos, path_neg, skin_label, non_skin_label):
        self.path_pos = path_pos
        self.path_neg = path_neg
        self.skin_label = skin_label
        self.non_skin_label = non_skin_label

    def __train_and_store_model(self, store_path, logger):
        trainer = HaralickModelTrainer(self.path_pos, self.path_neg, self.skin_label, self.non_skin_label, logger)
        trainer.train_and_store_model(store_path)

    @staticmethod
    def train_model(train_config=TextureTrainConfiguration(), logger=LogFactory.get_default_logger()):
        """
        Gets examples path from config, trains a svm then dumps the model in a file
        """
        logger.log("Started training texture model")
        trainer = TextureModelTrainer(
            train_config.path_pos, train_config.path_neg, train_config.skin_label, train_config.non_skin_label)
        trainer.__train_and_store_model(train_config.path_models + "/" + train_config.selected_classifier, logger)
        logger.log("Done")
