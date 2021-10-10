import preprocessing
import assymetry

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

# A, B, C, D = 0

if __name__=="__main__":
    original_img, img_gray, gauss_img, img_thresh, img_closing, ROI_img, max_contour, rectangle_coordinates = preprocessing.main_preprocessing()

    # A = assymetry.main()

    # Find center
    [center_x, center_y] = assymetry.find_center(max_contour)
    center = [center_x, center_y]

    # Check assymetry
    x, y, w, h = rectangle_coordinates
    cropped_img_closing = img_closing[y-offset_minus:y-offset_minus+h+offset_plus, x-offset_minus:x-offset_minus+w+offset_plus]

    A = assymetry.check_assymetry(cropped_img_closing)
    print(A)

    preprocessing.show_image("test1", ROI_img)
    preprocessing.show_image("test2", original_img)
