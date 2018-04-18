from color_analysis.detect.calculate.calculate_probability import ProbabilityCalculator
from utils.tuples import Pixel


class CachedProbabilityCalculator:
    """
    Calculates pixel probabilities and caches them
    """

    def __init__(self):
        self.pixel_probability_cache = {}

    def calculate_pixel_probability(self, pixel, bayes_spm_components, area):
        if area == 0:
            return ProbabilityCalculator.calculate_for_pixel(pixel, bayes_spm_components)
        else:
            p = Pixel(F1=pixel[0], F2=pixel[1], F3=pixel[2])
            if p in self.pixel_probability_cache:
                return self.pixel_probability_cache[p]
            else:
                prob = ProbabilityCalculator.calculate_max_from_area(
                    pixel, bayes_spm_components, area)
                self.pixel_probability_cache[p] = prob
                return prob
