import cv2
import numpy as np

from color_analysis.detect.detector import SpmDetectorFactory
from evaluator.calculate_results import Stats
from evaluator.run_configuration import RunConfiguration
from segmentation.quickshift import QuickshiftSegmentation
from texture_analysis.detect.detector import TextureDetectorFactory
from utils import general
from utils.log import LogFactory


class Evaluator:
    def __init__(self, config=RunConfiguration(), logger=LogFactory.get_default_logger()):
        logger.log('Initializing evaluator')

        self.config = config
        self.quickshift = QuickshiftSegmentation(config.qs_with_position,
                                                 config.qs_sigma,
                                                 config.qs_tau,
                                                 logger)
        self.spm_detector = SpmDetectorFactory.get_detector(config.spm_model_path,
                                                            config.spm_type,
                                                            config.spm_neighbour_area,
                                                            logger)
        self.texture_detector = TextureDetectorFactory.get_detector(config.texture_model_path,
                                                                    config.texture_detection_type,
                                                                    config.texture_detection_area,
                                                                    logger)
        self.logger = logger

    def run_detection(self):
        image = cv2.imread(self.config.detection_path)
        result = self.__process_image_detection(image)
        cv2.imwrite(self.config.results_path + '/' + self.config.detection_result_image_name, result)
        self.logger.log_done()

    def __process_image_detection(self, image):
        self.logger.log("Started image detection")

        if self.config.resize == 1:
            image = cv2.resize(image, self.config.size)

        if self.config.spm_type == 2:
            self.logger.log("Image segmentation")
            superpixels = self.quickshift.get_superpixels(image)

            self.logger.log("Applying Bayes SPM detection")
            spm_image = self.spm_detector.detect(image, superpixels, self.config.spm_threshold)
        else:
            self.logger.log("Applying quickshift algorithm")
            qs_image = self.quickshift.apply(image)

            self.logger.log("Applying Bayes SPM detection")
            spm_image = self.spm_detector.detect(qs_image, self.config.spm_threshold)

        self.logger.log("\nApplying Haralick texture detection")
        texture_image = self.texture_detector.detect_with_mask(image, spm_image)

        self.logger.log("\nCombining results")
        result = self.__combine_res(image, spm_image, texture_image)

        return result

    def run_validation(self):
        self.__clear_logs()
        self.__dump_config()

        self.logger.log('Loading images from folder')
        test_images = general.load_images_from_folder(self.config.test_path_in)
        expected_images = general.load_images_from_folder(self.config.test_path_expected)

        self.__print_header()

        for image_index in range(len(test_images)):
            test_image = test_images[image_index]
            expected_image = expected_images[image_index]

            if self.config.resize == 1:
                test_image = cv2.resize(test_image, self.config.size)
                expected_image = cv2.resize(expected_image, self.config.size)

            result = self.__process_image_evaluation(test_image, image_index)
            self.logger.log("\nComparing results")
            stats = Stats.get_stats(expected_image, result, image_index)
            self.logger.log(str(stats))
            self.__append_results(stats)
        self.logger.log_done()

    def __process_image_evaluation(self, image, image_index):
        self.logger.log("-----------------------------------------------------------")
        self.logger.log("Processing image : " + str(image_index))

        if self.config.spm_type == 2:
            self.logger.log("Image segmentation")
            superpixels = self.quickshift.get_superpixels(image)

            self.logger.log("Applying Bayes SPM detection")
            spm_image = self.spm_detector.detect(image, superpixels, self.config.spm_threshold)
            cv2.imwrite(self.config.results_path + '/' + str(image_index) + 'bayes_spm.png', spm_image)
        else:
            self.logger.log("Applying quickshift algorithm")
            qs_image = self.quickshift.apply(image)
            cv2.imwrite(self.config.results_path + '/' + str(image_index) + 'qs.png', qs_image)

            self.logger.log("Applying Bayes SPM detection")
            spm_image = self.spm_detector.detect(qs_image, self.config.spm_threshold)
            cv2.imwrite(self.config.results_path + '/' + str(image_index) + 'bayes_spm.png', spm_image)

        self.logger.log("\nApplying Haralick texture detection")
        texture_image = self.texture_detector.detect_with_mask(image, spm_image)

        cv2.imwrite(self.config.results_path + '/' + str(image_index) + 'texture.png', texture_image)

        self.logger.log("\nCombining results")
        result = self.__combine_res(image, spm_image, texture_image)
        cv2.imwrite(self.config.results_path + '/' + str(image_index) + 'result.png', result)

        return result

    def __print_header(self):
        with open(self.config.results_path + '/' + "results.txt", "w") as myfile:
            myfile.write(Stats.get_csv_header())

    def __append_results(self, stats):
        with open(self.config.results_path + '/' + "results.txt", "a") as myfile:
            myfile.write(stats.get_as_csv())

    def __dump_config(self):
        with open(self.config.results_path + '/' + "initial_config.txt", "w") as file:
            file.write(self.config.get_params_as_string())

    def __clear_logs(self):
        open(self.config.logging_path, 'w').close()

    def __combine_res(self, image, spm_img, texture_img):
        new_image = general.generate_overlay_image(image)

        rows = image.shape[0]
        cols = image.shape[1]
        for x_pixel in range(rows):
            for y_pixel in range(cols):
                if np.all(spm_img[x_pixel, y_pixel] == 0) and np.all(texture_img[x_pixel, y_pixel] == 0):
                    new_image[x_pixel, y_pixel] = [0, 0, 0]
        return new_image

if __name__ == '__main__':
    evaluator = Evaluator(RunConfiguration())
    evaluator.run_validation()
    # run_detection()
