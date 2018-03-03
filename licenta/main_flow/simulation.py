from quickshift_project.quickshift import quickshift_algorithm
from skin_probability_map.bayes.bayes_spm_operations import detect_skin_spm
from texture_detection.haralick import detect_skin_texture
from evaluator.combine_results import combine_res
from evaluator import run_config

import cv2


def run(image):
    print("Applying quickshift algorithm")
    qs_image = quickshift_algorithm(image, run_config.sigma, run_config.tau, run_config.with_position)
    cv2.imwrite('qs.png', qs_image)

    print("Applying Bayes SPM detection")
    spm_image = detect_skin_spm(qs_image,
                                run_config.spm_model_path,
                                run_config.threshold,
                                run_config.with_neighbours,
                                run_config.neighbour_area)
    cv2.imwrite('bayes_spm.png', spm_image)

    spm_image = cv2.imread('bayes_spm.png')
    print("Applying Haralick texture detection")
    texture_image = detect_skin_texture(image,
                                        run_config.texture_model_path,
                                        run_config.detection_type,
                                        run_config.window_size)
    cv2.imwrite('texture.png', texture_image)

    print("Combining results")
    result = combine_res(image, spm_image, texture_image)
    cv2.imwrite('result.png', result)


img = cv2.imread('test.jpg')
run(img)
