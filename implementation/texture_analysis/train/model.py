class TextureModel:
    """
    Model used for texture detection
    Encapsulates the feature extraction method and the classifier
    """

    def __init__(self, feature_extractor, classifier, skin_label):
        self.feature_extractor = feature_extractor
        self.classifier = classifier
        self.skin_label = skin_label

    def classify(self, image):
        features = self.feature_extractor.extract(image)
        return self.classifier.classify(features)
