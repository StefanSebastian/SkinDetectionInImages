from color_analysis.detect.detectors.average_on_superpixel_detector import AverageOnSuperpixelDetector
from color_analysis.detect.detectors.neighbour_detector import NeighbourDetector
from color_analysis.detect.detectors.simple_detector import SimpleDetector
from utils import serialization


class SpmDetectorFactory:
    @staticmethod
    def get_detector(model_path, detector_type, neighbour_area):
        model = serialization.load_object(model_path)
        if detector_type == 0:
            detector = SimpleDetector(model)
        elif detector_type == 1:
            detector = NeighbourDetector(model, neighbour_area)
        else:
            detector = AverageOnSuperpixelDetector(model, neighbour_area)
        return detector

