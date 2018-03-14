import cv2
from segmentation.quickshift import QuickshiftSegmentation

img = cv2.imread('../licenta/resources/input_data/PASCAL2007/baby.jpg')

#segmenter = QuickshiftSegmentation(1, 3, 5)
#res = segmenter.apply(img)
#cv2.imwrite("test.png", res)

from color_analysis.detect.detector import DetectorFactory
from utils import utils

from color_analysis.train.trainer import SPMModelTrainer

#SPMModelTrainer.train_model()

images = utils.load_images_from_folder('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/skin/input_qs')
detector = DetectorFactory.get_detector('color_analysis/models/spm_compaq_2000_ycbcr.pkl', 1, 2)
im = 0
for image in images:
    im += 1
    i = 0.3
    while i < 1.0:
        i += 0.05
        new_im = detector.detect(image, i)
        cv2.imwrite(
            'image' + str(im) + 'qs_' + str(format(i, '.2f')) + '_thresh_' + str(2) + '_neighb.png', new_im)
