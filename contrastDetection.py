# https://www.pyimagesearch.com/2021/01/25/detecting-low-contrast-images-with-opencv-scikit-image-and-python/?__s=ywjltk4ni0wd7tust8nx

from skimage.exposure import is_low_contrast
from imutils.paths import list_images
import imutils
import cv2

image = cv2.imread("static/image/dpc3-620001238.jpg")

# image = imutils.resize(image, width=1280)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# edged = cv2.Canny(blurred, 30, 150)
edged = cv2.Canny(gray, 30, 150)

cv2.imwrite("static/image/contrastNoBlur.jpg", edged)
cv2.imshow("Blurred", blurred)
cv2.imshow("Edge", edged)
cv2.waitKey(0)
