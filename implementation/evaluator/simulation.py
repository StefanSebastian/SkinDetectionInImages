import cv2
from comet_ml import Experiment

from evaluator import run_config
from utils import utils
from evaluator.combine_results import Combiner
from evaluator.calculate_results import Stats
from segmentation.quickshift import QuickshiftSegmentation
from color_analysis.detect.detector import SpmDetectorFactory
from texture_analysis.detect.detector import TextureDetectorFactory


#experiment = Experiment(api_key="EDskVxUYap8T2SWExETIl7iTN")


class Evaluator:
    def __init__(self):
        self.quickshift = QuickshiftSegmentation(run_config.with_position, run_config.sigma, run_config.tau)
        self.spm_detector = SpmDetectorFactory.get_detector(run_config.spm_model_path,
                                                            run_config.spm_type,
                                                            run_config.neighbour_area)
        self.texture_detector = TextureDetectorFactory.get_detector(run_config.texture_model_path,
                                                                    run_config.detection_type,
                                                                    run_config.window_size)

        hyper_params = {"qs_sigma": run_config.sigma,
                        "qs_tau": run_config.tau,
                        "bayes_threshold": run_config.threshold,
                        "spm_neighbour_area" : run_config.neighbour_area,
                        "haralick_window": run_config.window_size}
        #experiment.log_multiple_params(hyper_params)

    def process_image(self, image, image_index):
        print("-----------------------------------------------------------")
        print("Processing image : " + str(image_index))

        if run_config.spm_type == 2:
            print("Image segmentation")
            superpixels = self.quickshift.get_superpixels(image)

            print("Applying Bayes SPM detection")
            spm_image = self.spm_detector.detect(image, superpixels, run_config.threshold)
            cv2.imwrite(run_config.results_path + '/' + str(image_index) + 'bayes_spm.png', spm_image)
        else:
            print("Applying quickshift algorithm")
            qs_image = self.quickshift.apply(image)
            cv2.imwrite(run_config.results_path + '/' + str(image_index) + 'qs.png', qs_image)

            print("Applying Bayes SPM detection")
            spm_image = self.spm_detector.detect(qs_image, run_config.threshold)
            cv2.imwrite(run_config.results_path + '/' + str(image_index) + 'bayes_spm.png', spm_image)

        print("\nApplying Haralick texture detection")
        texture_image = self.texture_detector.detect_with_mask(image, spm_image)

        cv2.imwrite(run_config.results_path + '/' + str(image_index) + 'texture.png', texture_image)

        print("\nCombining results")
        result = Combiner.combine_res(image, spm_image, texture_image)
        cv2.imwrite(run_config.results_path + '/' + str(image_index) + 'result.png', result)

        return result

    def run_validation(self):
        self.__dump_config()

        test_images = utils.load_images_from_folder(run_config.test_path_in)
        expected_images = utils.load_images_from_folder(run_config.test_path_expected)

        self.__print_header()

        for image_index in range(len(test_images)):
            test_image = test_images[image_index]
            expected_image = expected_images[image_index]

            if run_config.resize == 1:
                test_image = cv2.resize(test_image, run_config.size)
                expected_image = cv2.resize(expected_image, run_config.size)

            result = self.process_image(test_image, image_index)
            print("\nComparing results")
            stats = Stats.get_stats(expected_image, result, image_index)
            print(stats)

            self.__append_results(stats)

            metrics = {"true_positive_rate" : stats.true_positive_rate,
                       "false_negative_rate" : stats.false_negative_rate}
            #experiment.log_multiple_metrics(metrics)
            #experiment.set_step(image_index + 1)

    def __print_header(self):
        with open(run_config.results_path + '/' + "results.txt", "w") as myfile:
            myfile.write(Stats.get_csv_header())

    def __append_results(self, stats):
        with open(run_config.results_path + '/' + "results.txt", "a") as myfile:
            myfile.write(stats.get_as_csv())

    def __dump_config(self):
        with open("run_config.py") as f:
            lines = f.readlines()
            with open(run_config.results_path + '/' + "initial_config.txt", "w") as f1:
                f1.writelines(lines)

    def run_detection(self):
        images = utils.load_images_from_folder(run_config.detection_path)

        image_index = 0
        for image in images:
            image_index += 1
            self.process_image(image, image_index)


evaluator = Evaluator()
evaluator.run_validation()
# run_detection()
