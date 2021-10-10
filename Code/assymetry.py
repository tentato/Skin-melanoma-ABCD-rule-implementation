import cv2

import numpy as np
import argparse
import time
import os
import itertools
import math

import numpy as np
import matplotlib.pyplot as plt

offset_minus = 50
offset_plus = offset_minus*2

def find_center(contour):
	Moment = cv2.moments(contour)
	centerX = int(Moment["m10"] / Moment["m00"])
	centerY = int(Moment["m01"] / Moment["m00"])
	return centerX, centerY

# TO BE DONE
# 1. Podziel obraz na 2 części, obróć jedną i porównaj histogramy, potem obróć o 90 stopni i powtórz
# 2. Obróć cały obraz o 180 stopni i porównaj histogramy, potem obróć obraz o 90 stopni i sprawdź asymetrie 
def check_assymetry(img):
    # G_X = cv2.reduce(img, 0 ,cv2.REDUCE_SUM, cv2.CV_32S)
    # G_X = cv2.reduce(img, 0 ,cv2.REDUCE_SUM, cv2.CV_32S)
    # G_X = cv2.reduce(img, 1, cv2.cv.CV_REDUCE_SUM)
    # G_Y = cv2.reduce(img, 1, cv2.cv.CV_REDUCE_SUM)
    G_X = cv2.reduce(img, 0, cv2.REDUCE_SUM, dtype=cv2.CV_32F)
    G_Y = cv2.reduce(img, 0, cv2.REDUCE_SUM, dtype=cv2.CV_32F)

    compare_val = cv2.compareHist(G_X ,G_Y ,cv2.HISTCMP_CORREL)
    return compare_val