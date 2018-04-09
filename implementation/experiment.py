import cv2

from utils.utils import load_images_from_folder
from segmentation.quickshift import QuickshiftSegmentation
from color_analysis.detect.detector import SpmDetectorFactory

from color_analysis.train.trainer import SPMModelTrainer
SPMModelTrainer.create_default_spm_trainer()

'''
qs = QuickshiftSegmentation(1, 3, 5)
detector = SpmDetectorFactory.get_detector('color_analysis/models/spm_compaq_2000_with_ns_ycbcr.pkl', 2, 2)
pascalim = load_images_from_folder('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/PASCAL2007')


image_index = 0
for image in pascalim:
    image_index += 1
    image = cv2.resize(image, (200, 200))

    superpixels = qs.get_superpixels(image)

    threshold = 0.1
    while threshold < 1:
        threshold += 0.05
        spmim = detector.detect(image, superpixels, threshold)
        cv2.imwrite(str(image_index) + '_' + str(threshold) + '.png', spmim)
'''