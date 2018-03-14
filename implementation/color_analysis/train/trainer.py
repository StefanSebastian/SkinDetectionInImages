from utils import serialization
from color_analysis import config
from color_analysis.train.sfa import SfaComponentExtractor
from color_analysis.train.compaq import CompaqComponentExtractor
from color_analysis.train.model import SPMModel


class SPMModelTrainer:
    def __init__(self, component_extractor, color_space):
        self.component_extractor = component_extractor
        self.color_space = color_space

    def train_and_store_model(self, store_path):
        components = self.component_extractor.extract_components()
        model = SPMModel(components, self.color_space)
        serialization.save_object(model, store_path)

    @staticmethod
    def train_model():
        """
        Default factory method ; uses values from config
        :return:
        """

        if config.database == 'compaq':
            extractor = CompaqComponentExtractor(config.path_compaq, config.color_space)
        else:
            extractor = SfaComponentExtractor(config.path_pos, config.path_neg, config.color_space)
        trainer = SPMModelTrainer(extractor, config.color_space)
        trainer.train_and_store_model(config.path_models + '/' + config.selected_model)
