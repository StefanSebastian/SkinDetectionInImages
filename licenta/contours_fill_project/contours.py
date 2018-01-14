import cv2


def get_image_contours(image):
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(im2, contours, -1, (0, 255, 0), 3)
    __get_contour_stats(contours)
    return contours


def __get_contour_stats(contours):
    print("Found : ", len(contours), " contours")
    one_point_contours = 0
    for i in range(len(contours)):
        contour = contours[i]
        if contour.shape[0] <= 2:
            one_point_contours += 1
    print(one_point_contours, " have 1 or 2 points")