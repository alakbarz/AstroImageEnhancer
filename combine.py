import cv2

alpha = 1
beta = 0.3
gamma = 0

img1 = cv2.imread("static/image/dpc3-620001238.jpg")
img2 = cv2.imread("static/image/contrast.jpg")

img1 = cv2.addWeighted(img1, alpha, img2, beta, gamma)

cv2.imwrite("static/image/bright.jpg", img1)