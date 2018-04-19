import cv2

image = cv2.imread('human_cat.jpg')

from texture_analysis.detect.detector import TextureDetectorFactory
det = TextureDetectorFactory.get_detector('E:/Info/anu3/Licenta-git-2/Licenta/implementation/texture_analysis/models/svm_classifier_1000data_5area.pkl', 1, 5)
