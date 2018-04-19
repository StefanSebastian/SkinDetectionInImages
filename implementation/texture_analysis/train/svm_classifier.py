from sklearn.svm import LinearSVC


class SvmClassifier:

    @staticmethod
    def train_svm_classifier(features, labels):
        """
        Trains a svm classifier for the given features/labels
        """
        svm_classifier = LinearSVC(random_state=9)
        svm_classifier.fit(features, labels)

        return svm_classifier
