# import the necessary packages
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import cv2
import matplotlib.pyplot as plt

image = cv2.imread('download.png',0)
plt.figure()
plt.imshow(image, cmap="gray")

roi = image[:40,:180]
plt.figure()
plt.imshow(roi, cmap="gray")

config = ("-l eng --oem 1 --psm 7")
text = pytesseract.image_to_string(roi, config=config)




