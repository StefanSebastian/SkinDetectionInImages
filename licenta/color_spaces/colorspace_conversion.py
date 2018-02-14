import cv2


def convert(image, colorspace):
    if colorspace == 'HSV':
        return cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    elif colorspace == 'YCrCb':
        return cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)


test_im = cv2.imread('../resources/results/quickshift/rgb_pos_as_features/human_cat_3_5.png')
res = convert(test_im, 'HSV')
cv2.imwrite('human_cat_3_5_hsv.png', res)