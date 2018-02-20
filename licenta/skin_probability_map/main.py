import cv2

from skin_probability_map.bayes import config
from skin_probability_map.bayes.bayes_spm_operations import get_bayes_spm, detect_skin

spm = get_bayes_spm('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/skin/sfa/SKIN/35',
                    'E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/skin/sfa/NS/35')
image = cv2.imread('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/skin/people3_5.png')

i = 0.3
while i < 1.0:
    i += 0.05
    new_im = detect_skin(image, spm, i)
    cv2.imwrite('qs_' + str(i) + 'thresh_with_neighb_' + str(config.neighbour_area) + '.png', new_im)
