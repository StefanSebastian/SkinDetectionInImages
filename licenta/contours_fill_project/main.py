import cv2
from contours_fill_project.contours import get_image_contours
from contours_fill_project.fill_contours import fill_contours_with_random_colors

img = cv2.imread('../resources/input_data/PASCAL2007/people.jpg')
contours = get_image_contours(img)
filled = fill_contours_with_random_colors(img, contours)
cv2.imwrite("contours.png", filled)
