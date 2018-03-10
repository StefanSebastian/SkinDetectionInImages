import cv2

from quickshift_project.quickshift import quickshift_algorithm, get_superpixels, extract_superpixels
from utils.serialization import load_object

img = cv2.imread('../resources/input_data/PASCAL2007/girl_drink.jpg')
img = cv2.resize(img, (200, 200))
#parents = load_object("parents.pkl")

superpixels = get_superpixels(img, 3, 5, 1)
print(superpixels)

#superpixels = extract_superpixels(img, parents)
#print(superpixels)

#res = quickshift_algorithm(img, 3, 5, 1)
#cv2.imwrite("girl_drink_3_5.png", res)


#superpixels = get_superpixels(img, 3, 5, 1)
#print(superpixels)
