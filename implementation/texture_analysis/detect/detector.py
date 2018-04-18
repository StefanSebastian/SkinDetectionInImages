from texture_analysis.detect.grid_detector import GridDetector
from texture_analysis.detect.per_pixel_detector import PerPixelDetector
from sklearn.externals import joblib


class TextureDetectorFactory:
    @staticmethod
    def get_detector(model_path, detection_type, detection_window_size):
        model = joblib.load(model_path)
        if detection_type == 0:
            return GridDetector(model, detection_window_size)
        else:
            return PerPixelDetector(model, detection_window_size)
