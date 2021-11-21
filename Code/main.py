import preprocessing
import assymetry
import border
import color

import sys

import cv2

import numpy as np
import argparse
import time
import os
import itertools
import math

import numpy as np
import matplotlib.pyplot as plt

open('C:/Users/alepa/Desktop/Inz/Code/log_file.txt', 'w').close()
log_file = open("C:/Users/alepa/Desktop/Inz/Code/log_file.txt", "a")

path = 'C:/Users/alepa/Desktop/Inz/Skin_melanoma/to_process/'

full_path = sys.argv[1]

A = 0.0
B = 0.0
C = 0.0

#############################
#####	Main function	#####
#############################

if __name__=="__main__":
    # for file in os.listdir(path):
    #     full_path = path + file
    original_img, img_gray, gauss_img, img_thresh, img_closing, ROI_img, max_contour, rectangle_coordinates = preprocessing.main_preprocessing(full_path, log_file)
    center = preprocessing.find_center(max_contour)
    A = assymetry.main_assymetry(max_contour, center, log_file)
    # B = border.main_border(original_img, center, max_contour)
    C = color.main_color(original_img, max_contour, log_file)


    # ROI_img = cv2.circle(ROI_img, center, 3, (0, 255, 0), -1)
    # preprocessing.show_image("Center", ROI_img)


    print("[Results] A=", A)
    print("[Results] B=", B)
    print("[Results] C=", C)
    print("")
    log_file.write("[Results] A={}\n".format(A))
    log_file.write("[Results] B={}\n".format(B))
    log_file.write("[Results] C={}\n".format(C))

    log_file.close()