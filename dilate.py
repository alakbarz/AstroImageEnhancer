# The following site was used as a tutorial:
# https://appdividend.com/2020/09/22/python-cv2-dilate-dilation-of-images-using-opencv/

import numpy as np
import cv2

print("Imported dilate")

kernelSize = 2

def dilateImage():
  img = cv2.imread("static/image/dpc3-620001238.jpg")

  kernel = np.ones((kernelSize, kernelSize), np.uint8)
  img = cv2.dilate(img, kernel, iterations = 1)

  cv2.imwrite("static/image/dilated.jpg", img)

dilateImage()