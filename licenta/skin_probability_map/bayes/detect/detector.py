from utils import serialization
from skin_probability_map.bayes.detect.simple_detector import SimpleDetector
from skin_probability_map.bayes.detect.neighbour_detector import NeighbourDetector


def get_detector(model_path, with_neighbours, neighbour_area):
    model = serialization.load_object(model_path)
    if with_neighbours == 0:
        detector = SimpleDetector(model)
    else:
        detector = NeighbourDetector(model, neighbour_area)
    return detector

