# https://www.pyimagesearch.com/2016/10/31/detecting-multiple-bright-spots-in-an-image-with-python-and-opencv/
from imutils import contours
from skimage import measure
import numpy as np
import imutils
import cv2

image = cv2.imread("capture2.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)

# cv2.threshold(input, threshold, maptovalue)
# thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.threshold(gray, 75, 255, cv2.THRESH_BINARY)[1]

cv2.imshow("Gray", gray)
cv2.imshow("Threshold", thresh)
cv2.waitKey(0)
