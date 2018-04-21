from color_analysis.train.compaq import CompaqComponentExtractor
from color_analysis.train.model import SPMModel
from color_analysis.train.sfa import SfaComponentExtractor
from color_analysis.train.train_config import SpmTrainConfiguration
from utils.log import LogFactory
from utils.serialization import SerializationUtils


class SPMModelTrainer:
    def __init__(self, component_extractor, color_space):
        self.component_extractor = component_extractor
        self.color_space = color_space

    def __train_and_store_model(self, store_path):
        components = self.component_extractor.extract_components()
        model = SPMModel(components, self.color_space)

        serializer = SerializationUtils()
        serializer.save_object(model, store_path)

    @staticmethod
    def train_spm_model(train_config=SpmTrainConfiguration(), logger=LogFactory.get_default_logger()):
        """
        Default factory method ; uses values from config
        """
        logger.log("Started training model")
        if train_config.database == 'compaq':
            extractor = CompaqComponentExtractor(train_config.path_compaq, train_config.color_space, logger)
        else:
            extractor = SfaComponentExtractor(train_config.path_pos, train_config.path_neg,
                                              train_config.color_space, logger)
        trainer = SPMModelTrainer(extractor, train_config.color_space)
        trainer.__train_and_store_model(train_config.path_models + '/' + train_config.selected_model)
