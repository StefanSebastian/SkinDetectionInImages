from color_analysis.detect.detectors.average_on_superpixel_detector import AverageOnSuperpixelDetector
from color_analysis.detect.detectors.neighbour_detector import NeighbourDetector
from color_analysis.detect.detectors.simple_detector import SimpleDetector
from utils import serialization
from utils.log import LogFactory


class SpmDetectorFactory:
    @staticmethod
    def get_detector(model_path, detector_type, neighbour_area, logger=LogFactory.get_default_logger()):
        model = serialization.load_object(model_path)
        if detector_type == 0:
            detector = SimpleDetector(model, logger)
        elif detector_type == 1:
            detector = NeighbourDetector(model, neighbour_area, logger)
        else:
            detector = AverageOnSuperpixelDetector(model, neighbour_area, logger)
        return detector

