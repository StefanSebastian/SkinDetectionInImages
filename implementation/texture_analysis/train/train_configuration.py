class TextureTrainConfiguration:
    def __init__(self,
                 path_pos='E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/skin/sfa/SKIN/5',
                 path_neg='E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/skin/sfa/NS/5',
                 path_models='E:/Info/anu3/Licenta-git-2/Licenta/implementation/texture_analysis/models',
                 skin_label='skin',
                 non_skin_label='ns',
                 selected_classifier='test_model.pkl'):
        self.path_pos = path_pos
        self.path_neg = path_neg
        self.path_models = path_models
        self.skin_label = skin_label
        self.non_skin_label = non_skin_label
        self.selected_classifier = selected_classifier
