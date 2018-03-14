from color_analysis.train import train_config
from color_analysis.train.compaq import CompaqComponentExtractor
from color_analysis.train.model import SPMModel
from color_analysis.train.sfa import SfaComponentExtractor
from utils import serialization


class SPMModelTrainer:
    def __init__(self, component_extractor, color_space):
        self.component_extractor = component_extractor
        self.color_space = color_space

    def train_and_store_model(self, store_path):
        components = self.component_extractor.extract_components()
        model = SPMModel(components, self.color_space)
        serialization.save_object(model, store_path)

    @staticmethod
    def create_default_spm_trainer():
        """
        Default factory method ; uses values from config
        :return:
        """

        if train_config.database == 'compaq':
            extractor = CompaqComponentExtractor(train_config.path_compaq, train_config.color_space)
        else:
            extractor = SfaComponentExtractor(train_config.path_pos, train_config.path_neg, train_config.color_space)
        trainer = SPMModelTrainer(extractor, train_config.color_space)
        trainer.train_and_store_model(train_config.path_models + '/' + train_config.selected_model)
