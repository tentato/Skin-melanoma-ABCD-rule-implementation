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
### White range = [any, 0:10, 95:100] 
white_range = [[0, 15], [240, 255]]
white_pixels_rate = 0.01
### Black range = [any, any, 0:45]
black_range = [0, 45]
black_pixels_rate = 0.01
### Red range = [0:x and 165:180, 125:255, 125:255]
# red_range = [[0, 10], [160, 180], [125, 255], [125, 255]]
red_range = [[0, 20], [320, 360], [50, 100], [50, 100]]
red_pixels_rate = 0.01
### Blue-gray = [95:110, 100:150, 100:150]
### Brown = [10:20, 125:255, 100:255]
###     Light brown = [10:20, 125:188, 177:255]
###     Dark brown = [10:20, 188:255, 100:177]

def find_pixels_inside_contour(img, cnt):
    pixels_inside_cnt = [] # musi byc jeden, zeby nie wychodzilo poza zakres
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
        if HSV_value[1] >= white_range[0][0] and HSV_value[1] <= white_range[0][1]:
            if HSV_value[2] >= white_range[1][0] and HSV_value[2] <= white_range[1][1]:
                count = count + 1

    if count >= pixels_number*white_pixels_rate:
        white_val = 1
    else:
        white_val = 0

    print("## White:")
    print("Count: ", count)
    print("White val: ", white_val)
    return white_val

def check_black_color(img, pixels_inside_cnt, pixels_number):
    count = 0
    for pixel in pixels_inside_cnt:
        HSV_value = img[pixel[1], pixel[0]]
        if HSV_value[2] >= black_range[0] and HSV_value[2] <= black_range[1]:
            count = count + 1

    if count >= pixels_number*black_pixels_rate:
        black_val = 1
    else:
        black_val = 0

    print("## Black:")
    print("Count: ", count)
    print("Black val: ", black_val)
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
                    ount = count + 1
            
        if HSV_value[0] >= red_range[1][0] and HSV_value[0] <= red_range[1][1]:
            if HSV_value[1] >= red_range[2][0] and HSV_value[1] <= red_range[2][1]:
                if HSV_value[2] >= red_range[3][0] and HSV_value[2] <= red_range[3][1]: 
                    count = count + 1

    if count >= pixels_number*red_pixels_rate:
        red_val = 1
    else:
        red_val = 0

    print("## Red:")
    print("Count: ", count)
    print("Red val: ", red_val)
    print("All pix: ", pixels_number)
    return red_val

def check_blue_gray_color(img, pixels_inside_cnt, pixels_number):
    blue_gray_val = 0
    return blue_gray_val

def check_light_brown_color(img, pixels_inside_cnt, pixels_number):
    light_brown = 0
    return light_brown

def check_dark_brown_color(img, pixels_inside_cnt, pixels_number):
    dark_brown_val = 0
    return dark_brown_val

def main_color(img, cnt):
    C = 0.0
    # print(img[100, 100])
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)    # This is not converting color type properly

    # Convert to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(img[100, 100])

    # Concert to HSV
    img = rgb2hsv(img)
    print(img[100, 100])

    pixels_inside_cnt, pixels_number = find_pixels_inside_contour(img, cnt)
    # C = C + check_white_color(img, pixels_inside_cnt, pixels_number)
    # C = C + check_black_color(img, pixels_inside_cnt, pixels_number)
    C = C + check_red_color(img, pixels_inside_cnt, pixels_number)
    C = C + check_blue_gray_color(img, pixels_inside_cnt, pixels_number)
    C = C + check_light_brown_color(img, pixels_inside_cnt, pixels_number)
    C = C + check_dark_brown_color(img, pixels_inside_cnt, pixels_number)

    C = C * 0.5
    print(C)
    return C