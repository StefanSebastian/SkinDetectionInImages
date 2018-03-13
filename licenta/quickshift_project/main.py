import cv2

from quickshift_project.quickshift import quickshift_algorithm, get_superpixels, extract_superpixels
from utils.serialization import load_object

img = cv2.imread('../resources/input_data/PASCAL2007/girl_drink.jpg')
img = cv2.resize(img, (200, 200))


superpixels = get_superpixels(img, 3, 5, 1)
print(superpixels)


'''

from utils import utils
images = utils.load_images_from_folder("E:/Info/anu3/Licenta-git-2/Licenta/licenta/resources/input_data/compaq-filtered/train/train_images")
index = 0
for image in images:
    index += 1
    image = cv2.resize(image, (200, 200))
    res = quickshift_algorithm(image, 3, 5, 1)
    cv2.imwrite("res/" + str(index) + ".png", res)
#res = quickshift_algorithm(img, 3, 5, 1)
#cv2.imwrite("girl_drink_3_5.png", res)


#superpixels = get_superpixels(img, 3, 5, 1)
#print(superpixels)
'''