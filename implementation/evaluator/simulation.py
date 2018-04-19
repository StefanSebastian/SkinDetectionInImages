import cv2

from evaluator.run_configuration import RunConfiguration
from utils import general
from evaluator.combine_results import Combiner
from evaluator.calculate_results import Stats
from segmentation.quickshift import QuickshiftSegmentation
from color_analysis.detect.detector import SpmDetectorFactory
from texture_analysis.detect.detector import TextureDetectorFactory
from utils.log import LogFactory


class Evaluator:
    def __init__(self, config, logger=LogFactory.get_default_logger()):
        logger.log('Initializing evaluator')

        self.config = config
        self.quickshift = QuickshiftSegmentation(config.qs_with_position, config.qs_sigma, config.qs_tau, logger)
        self.spm_detector = SpmDetectorFactory.get_detector(config.spm_model_path,
                                                            config.spm_type,
                                                            config.spm_neighbour_area,
                                                            logger)
        self.texture_detector = TextureDetectorFactory.get_detector(config.texture_model_path,
                                                                    config.texture_detection_type,
                                                                    config.texture_detection_area,
                                                                    logger)
        self.logger = logger

    def process_image(self, image, image_index):
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
        result = Combiner.combine_res(image, spm_image, texture_image)
        cv2.imwrite(self.config.results_path + '/' + str(image_index) + 'result.png', result)

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

            result = self.process_image(test_image, image_index)
            self.logger.log("\nComparing results")
            stats = Stats.get_stats(expected_image, result, image_index)
            self.logger.log(str(stats))
            self.__append_results(stats)

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

    def run_detection(self):
        images = general.load_images_from_folder(self.config.detection_path)

        image_index = 0
        for image in images:
            image_index += 1
            self.process_image(image, image_index)


#evaluator = Evaluator(RunConfiguration())
#evaluator.run_validation()
# run_detection()
