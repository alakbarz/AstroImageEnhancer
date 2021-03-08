import cv2
import numpy as np

print("Imported brightness")

def increaseBrightness(image, value):
  image = cv2.add(image, np.array([value]))
  return image