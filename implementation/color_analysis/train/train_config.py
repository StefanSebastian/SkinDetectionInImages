
class SpmTrainConfiguration:
    def __init__(self,
                 path_pos='E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/sfa/train/positive',
                 path_neg='E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/sfa/train/negative',
                 path_models='E:/Info/anu3/Licenta-git-2/Licenta/implementation/color_analysis/models',
                 selected_model='spm_compaq_2000_with_ns_4000_rgb.pkl',
                 path_compaq='E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/compaq-filtered-fin/train',
                 database='compaq',  # compaq or sfa
                 color_space='RGB'
                 ):
        self.path_pos = path_pos
        self.path_neg = path_neg
        self.path_models = path_models
        self.selected_model = selected_model
        self.path_compaq = path_compaq
        self.database = database
        self.color_space = color_space
