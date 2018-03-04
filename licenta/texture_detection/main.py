"""

Purpose of this script is to run experiments related to texture detection

"""

from sklearn.externals import joblib
import cv2

from texture_detection import haralick
from utils import utils

#haralick.train_model()

images = utils.load_images_from_folder('../resources/input_data/PASCAL2007')

i = 0
for image in images:
    i += 1
    res = haralick.detect_skin_texture(image, 'models/svm_classifier_1000data_5area.pkl', 1, 4)
    cv2.imwrite(str(i) + '.png', res)
