import cv2

from utils.utils import load_images_from_folder
from texture_analysis.train.trainer import TextureTrainer
TextureTrainer.train_default_model()

image = cv2.imread('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/PASCAL2007/baby.jpg')
image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)



'''
from skimage.feature import greycomatrix, greycoprops
image = cv2.imread('E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/PASCAL2007/baby.jpg')
image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
glcm = greycomatrix(image, [5], [0], 256, symmetric=True, normed=True)
features = [greycoprops(glcm, prop='contrast')[0][0], greycoprops(glcm, prop='homogeneity')[0][0],
                    greycoprops(glcm, prop='energy')[0][0]]
print(features)
print(greycoprops(glcm, prop='contrast'))'''