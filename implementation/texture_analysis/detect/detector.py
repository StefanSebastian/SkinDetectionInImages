from texture_analysis.detect.grid_detector import GridDetector
from texture_analysis.detect.per_pixel_detector import PerPixelDetector
from sklearn.externals import joblib

from utils.log import LogFactory
from utils.serialization import SerializationUtils


class TextureDetectorFactory:
    @staticmethod
    def get_detector(model_path, detection_type, detection_window_size, logger=LogFactory.get_default_logger()):
        serializator = SerializationUtils(logger)
        model = serializator.load_joblib_object(model_path)

        if detection_type == 0:
            return GridDetector(model, detection_window_size, logger)
        else:
            return PerPixelDetector(model, detection_window_size, logger)
