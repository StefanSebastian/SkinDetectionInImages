class RunConfiguration:
    def __init__(self,
                 qs_sigma=3,
                 qs_tau=5,
                 qs_with_position=1,
                 spm_model_path= 'E:/Info/anu3/Licenta-git-2/Licenta/implementation/color_analysis/models/spm_compaq_2000_with_ns_4000_rgb.pkl',
                 spm_threshold=0.1, # 0.167
                 spm_type=2,
                 spm_neighbour_area=4,
                 texture_model_path='E:/Info/anu3/Licenta-git-2/Licenta/implementation/texture_analysis/models/svm_classifier_1000data_5area.pkl',
                 texture_detection_type=1,
                 texture_detection_area=5,
                 resize=1,
                 size=(200, 200),
                 test_path_in='E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/compaq-filtered-fin/validate/input',
                 test_path_expected='E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/compaq-filtered-fin/validate/mask',
                 results_path='E:/Info/anu3/Licenta-git-2/Licenta/implementation/evaluator/run_results',
                 logging_path='E:/Info/anu3/Licenta-git-2/Licenta/implementation/evaluator/run_results/logs.txt',
                 detection_path='E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/PASCAL2007',
                 detection_result_image_name='result.png'):

        self.qs_sigma = qs_sigma
        self.qs_tau = qs_tau
        self.qs_with_position = qs_with_position

        self.spm_model_path = spm_model_path
        self.spm_threshold = spm_threshold
        self.spm_type = spm_type
        self.spm_neighbour_area = spm_neighbour_area

        #  texture params
        self.texture_model_path = texture_model_path
        self.texture_detection_type = texture_detection_type  # 0 - sliding window, 1 - builds windows around each pixel
        self.texture_detection_area = texture_detection_area

        #  image size
        self.resize = resize  # 0 for no resize ; 1 for resize
        self.size = size

        #  testing data
        self.test_path_in = test_path_in
        self.test_path_expected = test_path_expected

        #  results path
        self.results_path = results_path
        self.logging_path = logging_path

        #  path for images used in live detection, not for calculating stats
        self.detection_path = detection_path

        # detection result image name
        self.detection_result_image_name = detection_result_image_name

    def get_params_as_string(self):
        res = ''
        res += 'qs sigma : ' + str(self.qs_sigma) + '\n'
        res += 'qs tau : ' + str(self.qs_tau) + '\n'
        res += 'qs with position : ' + str(self.qs_with_position) + '\n'

        res += 'spm model path : ' + str(self.spm_model_path) + '\n'
        res += 'spm threshold : ' + str(self.spm_threshold) + '\n'
        res += 'spm type : ' + str(self.spm_type) + '\n'
        res += 'spm neighbour area : ' + str(self.spm_neighbour_area) + '\n'

        res += 'texture model path : ' + str(self.texture_model_path) + '\n'
        res += 'texture detection type : ' + str(self.texture_detection_type) + '\n'
        res += 'texture detection area : ' + str(self.texture_detection_area) + '\n'

        res += 'resize : ' + str(self.resize) + '\n'
        res += 'size : ' + str(self.size) + '\n'

        res += 'test path in : ' + str(self.test_path_in) + '\n'
        res += 'test path expected : ' + str(self.test_path_expected) + '\n'

        res += 'results path : ' + str(self.results_path) + '\n'
        res += 'detection path : ' + str(self.detection_path) + '\n'

        return res
