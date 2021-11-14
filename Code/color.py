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

### HSV values ###
#   H = [1,179] -> 0, 360
#   S = [0, 255] -> 0, 100
#   v = [0, 255] -> 0, 100
### White range = [any, 0:10, 0:10] 
### Black range = [any, any, 0:38]
### Red range = [0:x and 165:180, 125:255, 125:255]
### Blue-gray = [95:110, 100:150, 100:150]
### Brown = [10:20, 125:255, 100:255]
###     Light brown = [10:20, 125:188, 177:255]
###     Dark brown = [10:20, 188:255, 100:177]

def main_color(img, thresh, cnt):
    pixels_inside_cnt = []

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if cv2.pointPolygonTest(cnt, (j, i), False) >= 0:
                pixels_inside_cnt.append((j, i))

    print(pixels_inside_cnt)



    C = 0
    return C