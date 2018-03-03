"""

Purpose of this script is to run experiments related to texture detection

"""

from sklearn.externals import joblib
import cv2

from texture_detection import haralick
from utils import utils

#haralick.train_model()


svm_classifier = joblib.load('models/svm_classifier_1000.pkl')
images = utils.load_images_from_folder('../resources/input_data/PASCAL2007')

i = 0
for image in images:
    i += 1
    res = haralick.detect_skin_texture(image, 'models/svm_classifier_1000.pkl', 0, 3)
    cv2.imwrite(str(i) + '.png', res)
