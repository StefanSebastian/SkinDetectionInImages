from utils import utils
import cv2

images = utils.load_images_from_folder('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/compaq-filtered/validate/input')

from segmentation.quickshift import QuickshiftSegmentation
qs = QuickshiftSegmentation(1, 3, 5)

from color_analysis.detect.detector import SpmDetectorFactory
color_detector = SpmDetectorFactory.get_detector('E:/Info/anu3/Licenta-git-2/Licenta/implementation/color_analysis/models/spm_compaq_2000_with_ns_rgb.pkl', 2, 5)

for image_index in range(len(images)):
    image = images[image_index]
    image = cv2.resize(image, (200, 200))

    superpixels = qs.get_superpixels(image)
    threshold = 0.05
    while threshold < 1:
        new_im = color_detector.detect(image, superpixels, threshold)
        cv2.imwrite(str(image_index) + '_' + str(threshold) + '.png', new_im)
        threshold += 0.05

