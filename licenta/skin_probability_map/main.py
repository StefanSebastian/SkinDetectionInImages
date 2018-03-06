"""

Purpose of this script is to run experiments related to spm

"""



import cv2

from skin_probability_map.bayes import config
from skin_probability_map.bayes import bayes_spm_operations

from utils import serialization, utils

# image = cv2.imread('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/skin/people3_5.png')



#bayes_spm_operations.train_model()


#spm = serialization.load_object("bayes/models/spm_compaq_2000.pkl")
images = utils.load_images_from_folder('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/skin/input_qs')

im = 0
for image in images:
    im += 1
    i = 0.3
    while i < 1.0:
        i += 0.05
        new_im = bayes_spm_operations.detect_skin_spm(image, 'bayes/models/spm_compaq_2000.pkl', i, 1, 4)
        cv2.imwrite(
            'image' + str(im) + 'qs_' + str(format(i, '.2f')) + '_thresh_' + str(4) + '_neighb.png', new_im)
