import cv2

from color_analysis.detect.detector import SpmDetectorFactory
from segmentation.quickshift import QuickshiftSegmentation
from evaluator.run_configuration import RunConfiguration
from utils.log import ConsoleLogger
config = RunConfiguration()
img = cv2.imread('E://Info//anu3//Licenta-git-2//Licenta//licenta//resources//input_data//PASCAL2007//baby.jpg')
img = cv2.resize(img, (200, 200))

spm_qs_detector = SpmDetectorFactory.get_detector(config.spm_model_path,
                                                            config.spm_type,
                                                            config.spm_neighbour_area,
                                                            ConsoleLogger())
spm_detector = SpmDetectorFactory.get_detector(config.spm_model_path,
                                                            1,
                                                            4,
                                                            ConsoleLogger())
quickshift = QuickshiftSegmentation(config.qs_with_position,
                                         config.qs_sigma,
                                         config.qs_tau,
                                        ConsoleLogger())
res_nonqs = spm_detector.detect(img, 0.25)
cv2.imwrite('nonqs.png', res_nonqs)

superpixels = quickshift.get_superpixels(img)
res_qs = spm_qs_detector.detect(img, superpixels, 0.25)
cv2.imwrite('qs.png', res_qs)


