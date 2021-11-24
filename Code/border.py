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
    img_copy = img.copy()
    sum = 0
    count = 0
    for i in range(100):
        try:    # in case not enough pixels out of the contour
            sum += img_copy[pixel[1]-count, pixel[0]]
            count += 1
        except:
            break
    avg_out = sum / count
    return avg_out

def find_avg_in(pixel, center, img):
    img_copy = img.copy()
    sum = 0
    count = 0
    range_pixels = (center[1] - pixel[1]) / 2

     # checks all pixels between top pixel and center to get better average
    for i in range(int(range_pixels)):
        sum += img_copy[pixel[1]+count, pixel[0]]
        count += 1
    avg_in = sum / count
    return avg_in

#############################
#####	Main function	#####
#############################

def main_border(img, center, contours, log):
    B = 0.0
    angle = 45
    for i in range(7):
        im_copy = img.copy()
        (h, w) = im_copy.shape[:2]

        M = cv2.getRotationMatrix2D((center[0], center[1]), -angle, 1.0)
        im_copy = cv2.warpAffine(im_copy, M, (w, h))

        contour_rotated = preprocessing.rotate_contour(contours, angle, center)
        top_pixel = find_top_pixel(contour_rotated, center)
        im_copy = preprocessing.convert_to_grayscale(im_copy)
        im_copy = preprocessing.gaussian_blur(im_copy)

        # close to 0 - darker, close to 255 - lighter
        avg_out = find_avg_out(top_pixel, im_copy)
        avg_in = find_avg_in(top_pixel, center, im_copy)
        print(avg_out)
        print(avg_in)
        cv2.drawContours(im_copy, [contour_rotated], 0, (0, 255, 250), 1)
        
        cv2.circle(im_copy, top_pixel, 3, (0, 255, 0), -1)
        cv2.circle(im_copy, center, 3, (0, 255, 0), -1)
        preprocessing.show_image("Rotate {}".format(angle), im_copy)  

        # plt.plot(im_copy[top_pixel[1]-30:top_pixel[1]+30, center[0]])
        # plt.show()

        angle += 45
    exit()
    
    return B

    
    # img_gray = preprocessing.convert_to_grayscale(img)
    # img_gray = preprocessing.gaussian_blur(img_gray)
    # plt.plot(img_gray[center[0],:])
    # plt.show()