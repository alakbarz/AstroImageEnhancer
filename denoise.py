# Any comments in quotation marks are from the OpenCV-Python Tutorials that can be found at the link below
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_photo/py_non_local_means/py_non_local_means.html

# Denoising using the "Non-local Means Denoising algorithm"

import cv2

print("Imported denoise")

img = cv2.imread("static/image/dpc3-620001238.jpg")

output             = None     # Do not output image
strength           = 10       # Denoising filter strength
strengthColour     = strength # "Same as h, but for color images only"
templateWindowSize = 7        # "should be odd. (recommended 7)"
searchWindowSize   = 21       # "should be odd. (recommended 21)"

def denoise():  
  dst = cv2.fastNlMeansDenoisingColored(img,
                                        output,
                                        strength,
                                        strengthColour,
                                        templateWindowSize,
                                        searchWindowSize)

  cv2.imwrite("static/image/denoise.jpg", dst)

denoise()