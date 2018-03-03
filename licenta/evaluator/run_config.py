#  quickshift params
use_qs = 1
sigma = 3
tau = 5
with_position = 1

#  spm params
use_spm = 1
spm_model_path = 'E:/Info/anu3/Licenta-git-2/Licenta/licenta/skin_probability_map/bayes/models/spm_1000.pkl'
threshold = 0.9
with_neighbours = 1
neighbour_area = 8

#  texture params
use_texture = 1
texture_model_path = 'E:/Info/anu3/Licenta-git-2/Licenta/licenta/texture_detection/models/svm_classifier_1000.pkl'
detection_type = 0  # 0 - sliding window, 1 - builds windows around each pixel
window_size = 3

#  testing data
test_path_in = 'E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/sfa/validate/input'
test_path_expected = 'E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/sfa/validate/expected'

#  results path
results_path = 'E:/Info/anu3/Licenta-git-2/Licenta/licenta/evaluator/run_results'

#  image size
resize = 1  # 0 for no resize ; 1 for resize
size = (200, 200)
