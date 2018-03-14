from texture_analysis.train.haralick import HaralickModelTrainer
from texture_analysis.train import train_config


class TextureTrainer:
    def __init__(self, path_pos, path_neg, skin_label, non_skin_label):
        self.path_pos = path_pos
        self.path_neg = path_neg
        self.skin_label = skin_label
        self.non_skin_label = non_skin_label

    def train_and_store_model(self, store_path):
        trainer = HaralickModelTrainer(self.path_pos, self.path_neg, self.skin_label, self.non_skin_label)
        trainer.train_and_store_model(store_path)

    @staticmethod
    def train_default_model():
        """
        Gets examples path from config, trains a svm then dumps the model in a file
        """
        trainer = TextureTrainer(
            train_config.path_pos, train_config.path_neg, train_config.skin_label, train_config.non_skin_label)
        trainer.train_and_store_model(train_config.path_models + "/" + train_config.selected_classifier)

