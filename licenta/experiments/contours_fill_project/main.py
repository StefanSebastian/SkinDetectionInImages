import cv2
from contours_fill_project.contours import get_image_contours

from experiments.contours_fill_project.fill_contours import fill_contours_with_random_colors, fill_contours_with_super_pixels
from quickshift_project.quickshift import quickshift_algorithm

img = cv2.imread('../resources/input_data/PASCAL2007/human_cat.jpg')
super_pixels = quickshift_algorithm(img, 2, 4, 1)
cv2.imwrite("people_2_4.png", super_pixels)

contours = get_image_contours(img)
filled = fill_contours_with_super_pixels(img, contours, super_pixels)
random_filled = fill_contours_with_random_colors(img, contours)
cv2.imwrite("contours.png", filled)
cv2.imwrite("contours_test.png", random_filled)