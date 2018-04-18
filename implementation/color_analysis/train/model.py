class SPMModel:
    """
    The model used for Skin Probability Maps
    encodes components and color space used for training
    """

    def __init__(self, components, color_space):
        self.components = components
        self.color_space = color_space
