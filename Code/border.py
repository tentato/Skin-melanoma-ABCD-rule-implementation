import preprocessing

import cv2
import numpy as np
import argparse
import time
import os
import itertools
import math
import numpy as np
import matplotlib.pyplot as plt
from numpy import ones,vstack
from numpy.linalg import lstsq
from random import randrange
import matplotlib.pyplot as plt

def find_top_pixel(contour, center):
    x = center[0]
    current_min = 1000000
    for p in contour:
        px = p[0][0]
        py = p[0][1]
        if px == x:
            if py < current_min:
                current_min = py
    top_pixel = [x, current_min]
    return top_pixel

def find_avg_out(pixel, img):
    sum = 0
    i = 0
    for i in range(60):
        sum = sum + img[pixel[0], pixel[1]-30+i]
        i=i+1
    avg_out = sum/i
    return avg_out

def find_avg_in(pixel, img):
    avg_in = 0
    return avg_in

#############################
#####	Main function	#####
#############################

def main_border(img, center, contours):
    B = 0.0
    angle = 45
    for i in range(7):
        im_copy = img.copy()
        (h, w) = im_copy.shape[:2]

        M = cv2.getRotationMatrix2D((center[0], center[1]), -angle, 1.0)
        im_copy = cv2.warpAffine(im_copy, M, (w, h))

        contour_rotated = preprocessing.rotate_contour(contours, angle, center)
        # cv2.drawContours(im_copy, [contour_rotated], 0, (0, 255, 250), 1)
        preprocessing.show_image("Rotate {}".format(angle), im_copy)  
        angle += 45
        top_pixel = find_top_pixel(contour_rotated, center)
        im_copy = preprocessing.convert_to_grayscale(im_copy)
        im_copy = preprocessing.gaussian_blur(im_copy)
        avg_out = find_avg_out(top_pixel, im_copy)
        print(avg_out)
        # plt.plot(im_copy[top_pixel[1]-30:top_pixel[1]+30, center[0]])
        # plt.show()
    return B

    
    # img_gray = preprocessing.convert_to_grayscale(img)
    # img_gray = preprocessing.gaussian_blur(img_gray)
    # plt.plot(img_gray[center[0],:])
    # plt.show()