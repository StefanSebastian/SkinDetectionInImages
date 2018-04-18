from utils.utils import load_images_from_folder

images = load_images_from_folder('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/PASCAL2007')
import cv2
from color_analysis.detect.detectors import SpmDetectorFactory
detector = SpmDetectorFactory.get_detector('E:/Info/anu3/Licenta-git-2/Licenta/implementation/color_analysis/models/spm_compaq_2000_with_ns_4000_rgb.pkl', 2, 4)

from segmentation.quickshift import QuickshiftSegmentation
qs = QuickshiftSegmentation(1, 3, 5)

im_index = 0
for image in images:
    image = cv2.resize(image, (200, 200))

    superpixels = qs.get_superpixels(image)

    im_index += 1
    thresh = 0
    while thresh < 0.5:
        thresh += 0.05

        detected = detector.detect(image, superpixels, thresh)
        cv2.imwrite(str(im_index) + '_' + str(thresh) + '.png', detected)
