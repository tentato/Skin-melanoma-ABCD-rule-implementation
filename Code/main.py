import preprocessing
import assymetry
import border

import cv2

import numpy as np
import argparse
import time
import os
import itertools
import math

import numpy as np
import matplotlib.pyplot as plt

path = 'C:/Users/alepa/Desktop/Inz/Skin melanoma/to process/'

A = 0
B = 0
C = 0
D = 0

if __name__=="__main__":
    for file in os.listdir(path):
        full_path = path + file
        original_img, img_gray, gauss_img, img_thresh, img_closing, ROI_img, max_contour, rectangle_coordinates = preprocessing.main_preprocessing(full_path)
        center = preprocessing.find_center(max_contour)
        A = assymetry.main_assymetry(max_contour, center)
        B = border.main_border(ROI_img, center, max_contour)

        ROI_img = cv2.circle(ROI_img, center, 3, (0, 255, 0), -1)
        preprocessing.show_image("Center", ROI_img)