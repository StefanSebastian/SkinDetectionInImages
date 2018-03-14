from utils import serialization
from color_analysis.detect.simple_detector import SimpleDetector
from color_analysis.detect.neighbour_detector import NeighbourDetector


class SpmDetectorFactory:
    @staticmethod
    def get_detector(model_path, with_neighbours, neighbour_area):
        model = serialization.load_object(model_path)
        if with_neighbours == 0:
            detector = SimpleDetector(model)
        else:
            detector = NeighbourDetector(model, neighbour_area)
        return detector

