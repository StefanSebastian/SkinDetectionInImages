import cv2

from utils import utils

from color_analysis.detect.detector import SpmDetectorFactory
from segmentation.quickshift import QuickshiftSegmentation

images = utils.load_images_from_folder('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/PASCAL2007')
detector = SpmDetectorFactory.get_detector('color_analysis/models/spm_compaq_2000_ycbcr.pkl', 2,0)
qs = QuickshiftSegmentation(1, 3, 5)
index = 0
for image in images:
    index += 1

    image = cv2.resize(image, (200, 200))
    superpixels = qs.get_superpixels(image)

    i = 0.1
    while i < 1:
        result = detector.detect(image, superpixels, i)
        cv2.imwrite(str(index) + '_' + str(i) + '.png', result)
        i += 0.1



'''
from texture_analysis.train.trainer import TextureTrainer

#TextureTrainer.train_default_model()

from texture_analysis.detect.detector import TextureDetectorFactory

detector = TextureDetectorFactory.get_detector('texture_analysis/models/svm_classifier_1000data_5area.pkl', 1, 3)
images = utils.load_images_from_folder('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/PASCAL2007')
im = 0
for image in images:
    image = cv2.resize(image, (200, 200))
    new_im = detector.detect(image)
    im += 1
    cv2.imwrite('image' + str(im) + ".png", new_im)
'''