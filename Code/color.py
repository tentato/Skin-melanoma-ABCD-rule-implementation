import preprocessing
import assymetry
import border
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
from skimage.color import rgb2hsv

### HSV values ###
#   H = [0.0, 1.0] -> 0, 360
#   S = [0.0, 1.0] -> 0, 100
#   v = [0.0, 1.0] -> 0, 100

###     White range
white_range = [[0, 10], [95, 100]]
white_pixels_rate = 0.01
###     Black range
black_range = [0, 20]
black_pixels_rate = 0.01
###     Red range
red_range = [[0, 20], [320, 360], [50, 100], [50, 100]]
red_pixels_rate = 0.01
###     Blue-gray
blue_gray_range = [[190, 220], [30, 70], [20, 70]]
blue_gray_pixels_rate = 0.01
###     Light brown
light_brown_range = [[20, 40], [25, 75], [55, 90]]
light_brown_pixels_rate = 0.01
###     Dark brown
dark_brown_range = [[20, 40], [25, 100], [20, 55]]
dark_brown_pixels_rate = 0.01

def find_pixels_inside_contour(img, cnt):
    pixels_inside_cnt = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if cv2.pointPolygonTest(cnt, (j, i), False) > 0:
                pixels_inside_cnt.append((j, i))

    pixels_number = len(pixels_inside_cnt)
    return pixels_inside_cnt, pixels_number

def check_white_color(img, pixels_inside_cnt, pixels_number):
    count = 0
    for pixel in pixels_inside_cnt:
        HSV_value = img[pixel[1], pixel[0]]
        HSV_value[0] = HSV_value[0] * 360
        HSV_value[1] = HSV_value[1] * 100
        HSV_value[2] = HSV_value[2] * 100
        if HSV_value[1] >= white_range[0][0] and HSV_value[1] <= white_range[0][1]:
            if HSV_value[2] >= white_range[1][0] and HSV_value[2] <= white_range[1][1]:
                count = count + 1

    if count >= pixels_number*white_pixels_rate:
        white_val = 1
    else:
        white_val = 0

    print("[INFO] All pixels: ", pixels_number)
    print("[INFO] White value: ", count)
    return white_val

def check_black_color(img, pixels_inside_cnt, pixels_number):
    count = 0
    for pixel in pixels_inside_cnt:
        HSV_value = img[pixel[1], pixel[0]]
        HSV_value[0] = HSV_value[0] * 360
        HSV_value[1] = HSV_value[1] * 100
        HSV_value[2] = HSV_value[2] * 100
        if HSV_value[2] >= black_range[0] and HSV_value[2] <= black_range[1]:
            count = count + 1

    if count >= pixels_number*black_pixels_rate:
        black_val = 1
    else:
        black_val = 0

    print("[INFO] Black value: ", count)
    return black_val

def check_red_color(img, pixels_inside_cnt, pixels_number):
    count = 0
    for pixel in pixels_inside_cnt:
        HSV_value = img[pixel[1], pixel[0]]
        HSV_value[0] = HSV_value[0] * 360
        HSV_value[1] = HSV_value[1] * 100
        HSV_value[2] = HSV_value[2] * 100
        if HSV_value[0] >= red_range[0][0] and HSV_value[0] <= red_range[0][1]:
            if HSV_value[1] >= red_range[2][0] and HSV_value[1] <= red_range[2][1]:
                if HSV_value[2] >= red_range[3][0] and HSV_value[2] <= red_range[3][1]: 
                    count = count + 1
            
        if HSV_value[0] >= red_range[1][0] and HSV_value[0] <= red_range[1][1]:
            if HSV_value[1] >= red_range[2][0] and HSV_value[1] <= red_range[2][1]:
                if HSV_value[2] >= red_range[3][0] and HSV_value[2] <= red_range[3][1]: 
                    count = count + 1

    if count >= pixels_number*red_pixels_rate:
        red_val = 1
    else:
        red_val = 0

    print("[INFO] Red value: ", count)
    return red_val

def check_blue_gray_color(img, pixels_inside_cnt, pixels_number):
    count = 0
    for pixel in pixels_inside_cnt:
        HSV_value = img[pixel[1], pixel[0]]
        HSV_value[0] = HSV_value[0] * 360
        HSV_value[1] = HSV_value[1] * 100
        HSV_value[2] = HSV_value[2] * 100
        if HSV_value[0] >= blue_gray_range[0][0] and HSV_value[0] <= blue_gray_range[0][1]:
            if HSV_value[1] >= blue_gray_range[1][0] and HSV_value[1] <= blue_gray_range[1][1]:
                if HSV_value[2] >= blue_gray_range[2][0] and HSV_value[2] <= blue_gray_range[2][1]: 
                    count = count + 1

    if count >= pixels_number*blue_gray_pixels_rate:
        blue_gray_val = 1
    else:
        blue_gray_val = 0

    print("[INFO] Blue-gray value: ", count)
    return blue_gray_val

def check_light_brown_color(img, pixels_inside_cnt, pixels_number):
    count = 0
    for pixel in pixels_inside_cnt:
        HSV_value = img[pixel[1], pixel[0]]
        HSV_value[0] = HSV_value[0] * 360
        HSV_value[1] = HSV_value[1] * 100
        HSV_value[2] = HSV_value[2] * 100
        if HSV_value[0] >= light_brown_range[0][0] and HSV_value[0] <= light_brown_range[0][1]:
            if HSV_value[1] >= light_brown_range[1][0] and HSV_value[1] <= light_brown_range[1][1]:
                if HSV_value[2] >= light_brown_range[2][0] and HSV_value[2] <= light_brown_range[2][1]:
                    count = count + 1

    if count >= pixels_number*light_brown_pixels_rate:
        light_brown_val = 1
    else:
        light_brown_val = 0

    print("[INFO] Light brown value: ", count)
    return light_brown_val

def check_dark_brown_color(img, pixels_inside_cnt, pixels_number):
    count = 0
    for pixel in pixels_inside_cnt:
        HSV_value = img[pixel[1], pixel[0]]
        HSV_value[0] = HSV_value[0] * 360
        HSV_value[1] = HSV_value[1] * 100
        HSV_value[2] = HSV_value[2] * 100
        if HSV_value[0] >= dark_brown_range[0][0] and HSV_value[0] <= dark_brown_range[0][1]:
            if HSV_value[1] >= dark_brown_range[1][0] and HSV_value[1] <= dark_brown_range[1][1]:
                if HSV_value[2] >= dark_brown_range[2][0] and HSV_value[2] <= dark_brown_range[2][1]:
                    count = count + 1

    if count >= pixels_number*dark_brown_pixels_rate:
        dark_brown_val = 1
    else:
        dark_brown_val = 0

    print("[INFO] Dark brown value: ", count)
    return dark_brown_val

#############################
#####	Main function	#####
#############################

def main_color(img, cnt):
    C = 0.0
    print("[INFO] COLOR RECOGNITION STARTED")


    pixels_inside_cnt, pixels_number = find_pixels_inside_contour(img, cnt)

    # Convert to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Concert to HSV
    img = rgb2hsv(img)

    copy_img = img.copy()
    white = check_white_color(copy_img, pixels_inside_cnt, pixels_number)

    copy_img = img.copy()
    black = check_black_color(copy_img, pixels_inside_cnt, pixels_number)

    copy_img = img.copy()
    blue_gray = check_blue_gray_color(copy_img, pixels_inside_cnt, pixels_number)

    copy_img = img.copy()
    red = check_red_color(copy_img, pixels_inside_cnt, pixels_number)

    copy_img = img.copy()
    light_brown = check_light_brown_color(copy_img, pixels_inside_cnt, pixels_number)

    copy_img = img.copy()
    dark_brown = check_dark_brown_color(copy_img, pixels_inside_cnt, pixels_number)

    C = (white + black + red + blue_gray + light_brown + dark_brown) * 0.5
    print("[INFO] COLOR RECOGNITION FINISHED\n")
    return C