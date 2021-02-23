# https://github.com/maitek/image_stacking
import os
import cv2
import numpy as np

imageDirectory = "testSet"

files = os.listdir(imageDirectory)
files = [os.path.join(imageDirectory, x) for x in files if x.endswith(('.jpg'))]

print(files)

def stackImagesECC(files):
    M = np.eye(3, 3, dtype=np.float32)

    first_image = None
    stacked_image = None

    for file in files:
        image = cv2.imread(file, 1).astype(np.float32) / 255
        print(file)
        if first_image is None:
            # convert to gray scale floating point image
            first_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            stacked_image = image
        else:
            # Estimate perspective transform
            criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 3000,  1e-5)
            s, M = cv2.findTransformECC(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), first_image, M, cv2.MOTION_HOMOGRAPHY, criteria, None, 5)
            w, h, _ = image.shape
            # Align image to first image
            image = cv2.warpPerspective(image, M, (h, w))
            stacked_image += image

    stacked_image /= len(files)
    stacked_image = (stacked_image*255).astype(np.uint8)
    return stacked_image


stackedImaged = stackImagesECC(files)
cv2.imwrite("stacked.jpg", stackedImaged)
