import numpy as np
import cv2
import os

#load cascade classifier training file for haarcascade
haar_face_cascade = cv2.CascadeClassifier('haar_cascade.xml')

resource_dir = '../resources/input_data/PASCAL2007'


def detect_faces(f_cascade, colored_img, scaleFactor=1.1):
    # just making a copy of image passed, so that passed image is not changed
    img_copy = colored_img.copy()

    # convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    # let's detect multiscale (some images may be closer to camera than others) images
    faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5)

    print("Found", len(faces), "faces")

    # go over list of faces and draw them as rectangles on original colored img
    for (x, y, w, h) in faces:
        cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return img_copy

for filename in os.listdir(resource_dir):
    if filename.endswith(".jpg"):
        path = os.path.join(resource_dir, filename)
        print(path)
        img = cv2.imread(path)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        i = 1
        while i <= 2:
            i += 0.05
            faces_im = detect_faces(haar_face_cascade, img, i)

            res_path = "results/scale" + str(i)
            if not os.path.exists(res_path):
                os.mkdir(res_path)
            cv2.imwrite(res_path + "/" + filename, faces_im)

