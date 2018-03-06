from quickshift_project.quickshift import quickshift_algorithm
from skin_probability_map.bayes.bayes_spm_operations import detect_skin_spm
from texture_detection.haralick import detect_skin_texture
from evaluator.combine_results import combine_res
from evaluator import run_config
from evaluator import calculate_results
from utils import utils

import cv2


def process_image(image, image_index):
    print("-----------------------------------------------------------")
    print("Processing image : " + str(image_index))

    print("Applying quickshift algorithm")
    qs_image = quickshift_algorithm(image, run_config.sigma, run_config.tau, run_config.with_position)
    cv2.imwrite(run_config.results_path + '/' + str(image_index) + 'qs.png', qs_image)

    print("Applying Bayes SPM detection")
    spm_image = detect_skin_spm(qs_image,
                                run_config.spm_model_path,
                                run_config.threshold,
                                run_config.with_neighbours,
                                run_config.neighbour_area)
    cv2.imwrite(run_config.results_path + '/' + str(image_index) + 'bayes_spm.png', spm_image)

    print("\nApplying Haralick texture detection")
    texture_image = detect_skin_texture(image,
                                        run_config.texture_model_path,
                                        run_config.detection_type,
                                        run_config.window_size)
    cv2.imwrite(run_config.results_path + '/' + str(image_index) + 'texture.png', texture_image)

    print("\nCombining results")
    result = combine_res(image, spm_image, texture_image)
    cv2.imwrite(run_config.results_path + '/' + str(image_index) + 'result.png', result)

    return result


def run_validation():
    __dump_config()

    test_images = utils.load_images_from_folder(run_config.test_path_in)
    expected_images = utils.load_images_from_folder(run_config.test_path_expected)

    __print_header()

    for image_index in range(len(test_images)):
        test_image = test_images[image_index]
        expected_image = expected_images[image_index]

        if run_config.resize == 1:
            test_image = cv2.resize(test_image, run_config.size)
            expected_image = cv2.resize(expected_image, run_config.size)

        result = process_image(test_image, image_index)
        print("\nComparing results")
        stats = calculate_results.get_stats(expected_image, result, image_index)
        print(stats)

        __append_results(stats)


def __print_header():
    with open(run_config.results_path + '/' + "results.txt", "w") as myfile:
        myfile.write(calculate_results.Stats.get_csv_header())


def __append_results(stats):
    with open(run_config.results_path + '/' + "results.txt", "a") as myfile:
        myfile.write(stats.get_as_csv())


def __dump_config():
    with open("run_config.py") as f:
        lines = f.readlines()
        with open(run_config.results_path + '/' + "initial_config.txt", "w") as f1:
            f1.writelines(lines)


def run_detection():
    images = utils.load_images_from_folder(run_config.detection_path)

    image_index = 0
    for image in images:
        image_index += 1
        process_image(image, image_index)


#run_validation()
run_detection()