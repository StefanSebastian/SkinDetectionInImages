"""

Purpose of this script is to run experiments related to spm

"""
from utils import utils
import cv2
from skin_probability_map.bayes.train import trainer
from skin_probability_map.bayes.detect import detector

#trainer.train_model()

images = utils.load_images_from_folder('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/skin/input_qs')
detector = detector.get_detector('bayes/models/spm_compaq_2000_ycbcr.pkl', 1, 8)

im = 0
for image in images:
    im += 1
    i = 0.3
    while i < 1.0:
        i += 0.05
        new_im = detector.detect(image, i)
        cv2.imwrite(
            'image' + str(im) + 'qs_' + str(format(i, '.2f')) + '_thresh_' + str(8) + '_neighb.png', new_im)

