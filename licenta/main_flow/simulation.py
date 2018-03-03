from quickshift_project.quickshift import quickshift_algorithm_default
from skin_probability_map.bayes.bayes_spm_operations import detect_skin_spm_default
from texture_detection.haralick import detect_skin_texture_default
from main_flow.combine_results import combine_res

import cv2


def run(image):
    print("Applying quickshift algorithm")
    qs_image = quickshift_algorithm_default(image)
    cv2.imwrite('qs.png', qs_image)

    print("Applying Bayes SPM detection")
    spm_image = detect_skin_spm_default(qs_image)
    cv2.imwrite('bayes_spm.png', spm_image)

    print("Applying Haralick texture detection")
    texture_image = detect_skin_texture_default(image)
    cv2.imwrite('texture.png', texture_image)

    print("Combining results")
    result = combine_res(image, spm_image, texture_image)
    cv2.imwrite('result.png', result)

img = cv2.imread('test.jpg')
run(img)
