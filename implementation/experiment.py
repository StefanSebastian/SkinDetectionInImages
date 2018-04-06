import numpy as np
import cv2
from utils.utils import load_images_from_folder
from texture_analysis.detect.detector import TextureDetectorFactory
from utils import utils
# import the necessary packages
from skimage import feature
from sklearn.svm import LinearSVC

class LocalBinaryPatterns:
    def __init__(self, numPoints, radius):
        # store the number of points and radius
        self.numPoints = numPoints
        self.radius = radius

    def describe(self, image, eps=1e-7):
        # compute the Local Binary Pattern representation
        # of the image, and then use the LBP representation
        # to build the histogram of patterns
        lbp = feature.local_binary_pattern(image, self.numPoints,
                                           self.radius, method="uniform")
        (hist, _) = np.histogram(lbp.ravel(),
                                 bins=np.arange(0, self.numPoints + 3),
                                 range=(0, self.numPoints + 2))

        # normalize the histogram
        hist = hist.astype("float")
        hist /= (hist.sum() + eps)

        # return the histogram of Local Binary Patterns
        return hist

desc = LocalBinaryPatterns(6, 3)
data = []
labels = []

images = utils.load_images_from_folder('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/skin/sfa/SKIN/7')
for image in images:
    # load the image, convert it to grayscale, and describe it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = desc.describe(gray)

    # extract the label from the image path, then update the
    # label and data lists
    labels.append("SKIN")
    data.append(hist)

images = utils.load_images_from_folder('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/skin/sfa/NS/7')
for image in images:
    # load the image, convert it to grayscale, and describe it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = desc.describe(gray)

    # extract the label from the image path, then update the
    # label and data lists
    labels.append("NS")
    data.append(hist)

model = LinearSVC(C=100.0, random_state=42)
model.fit(data, labels)

# loop over the testing images
images = utils.load_images_from_folder('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/PASCAL2007')
idx = 0
for image in images:
    idx += 1
    new_image = utils.generate_overlay_image(image)

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    rows = gray.shape[0]
    cols = gray.shape[1]

    radius = 3
    for x_pixel in range(radius, rows - radius):
        for y_pixel in range(radius, cols - radius):
            utils.print_progress_pixel(x_pixel, y_pixel, rows, cols)

            r = x_pixel - radius
            c = y_pixel - radius
            grid_size = 2 * radius + 1
            roi = gray[r:r + grid_size, c:c + grid_size]

            hist = desc.describe(roi)
            prediction = model.predict(hist.reshape(1, -1))[0]
            if prediction == "SKIN":
                new_image[x_pixel, y_pixel] = [0, 0, 0]
    cv2.imwrite(str(idx) + '.png', new_image)
    print("----------")


'''
import cv2

from utils import utils

from color_analysis.detect.detector import SpmDetectorFactory
from segmentation.quickshift import QuickshiftSegmentation

#images = utils.load_images_from_folder('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/PASCAL2007')
images = utils.load_images_from_folder('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/compaq-filtered/validate/input')
detector = SpmDetectorFactory.get_detector('color_analysis/models/spm_compaq_2000_ycbcr.pkl', 2, 5)
qs = QuickshiftSegmentation(1, 3, 5)
index = 0
for image in images:
    index += 1

    image = cv2.resize(image, (200, 200))
    superpixels = qs.get_superpixels(image)

    i = 0.1
    while i < 1:
        result = detector.detect(image, superpixels, i)
        cv2.imwrite(str(index) + '_' + str(i) + '.png', result)
        i += 0.1

'''

'''
from texture_analysis.train.trainer import TextureTrainer

#TextureTrainer.train_default_model()

from texture_analysis.detect.detector import TextureDetectorFactory

detector = TextureDetectorFactory.get_detector('texture_analysis/models/svm_classifier_1000data_5area.pkl', 1, 3)
images = utils.load_images_from_folder('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/PASCAL2007')
im = 0
for image in images:
    image = cv2.resize(image, (200, 200))
    new_im = detector.detect(image)
    im += 1
    cv2.imwrite('image' + str(im) + ".png", new_im)
'''