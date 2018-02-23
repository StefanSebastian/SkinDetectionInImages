from sklearn.externals import joblib
import cv2

from texture_detection import haralick
from utils import utils

svm_classifier = joblib.load('svm_classifier.pkl')
images = utils.load_images_from_folder('../resources/input_data/PASCAL2007')

i = 0
for image in images:
    i += 1
    res = haralick.get_image_skin_regions(svm_classifier, image, 15)
    cv2.imwrite(str(i) + '.png', res)
