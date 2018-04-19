#  quickshift params
qs_sigma = 3
qs_tau = 5
qs_with_position = 1

#  spm params
spm_model_path = 'E:/Info/anu3/Licenta-git-2/Licenta/implementation/color_analysis/models/spm_compaq_2000_with_ns_4000_rgb.pkl'
spm_threshold = 0.167
spm_type = 2
spm_neighbour_area = 4

#  texture params
texture_model_path = 'E:/Info/anu3/Licenta-git-2/Licenta/implementation/texture_analysis/models/svm_classifier_1000data_5area.pkl'
texture_detection_type = 1  # 0 - sliding window, 1 - builds windows around each pixel
texture_detection_area = 5

#  image size
resize = 1  # 0 for no resize ; 1 for resize
size = (200, 200)

#  testing data
test_path_in = 'E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/compaq-filtered-fin/validate/input'
test_path_expected = 'E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/compaq-filtered-fin/validate/mask'

#  results path
results_path = 'E:/Info/anu3/Licenta-git-2/Licenta/implementation/evaluator/run_results'

#  path for images used in live detection, not for calculating stats
detection_path = 'E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/PASCAL2007'
