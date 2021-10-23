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

def cartesian2polar(x, y):
    theta = np.arctan2(y, x)
    rho = np.hypot(x, y)
    return theta, rho

def polar2cartesian(theta, rho):
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y


def rotate_contour(contour, angle, center):
    cx = center[0]
    cy = center[1]

    contour_norm = contour - [cx, cy]
    
    coordinates = contour_norm[:, 0, :]
    xs, ys = coordinates[:, 0], coordinates[:, 1]
    thetas, rhos = cartesian2polar(xs, ys)
    
    thetas = np.rad2deg(thetas)
    thetas = (thetas + angle) % 360
    thetas = np.deg2rad(thetas)
    
    xs, ys = polar2cartesian(thetas, rhos)
    
    contour_norm[:, 0, 0] = xs
    contour_norm[:, 0, 1] = ys

    contour_rotated = contour_norm + [cx, cy]
    contour_rotated = contour_rotated.astype(np.int32)

    return contour_rotated


#############################
#####	Main function	#####
#############################

def main_border(img, center, contours):
    B = 0
    # img_gray = preprocessing.convert_to_grayscale(img)
    # img_gray = preprocessing.gaussian_blur(img_gray)
    # plt.plot(img_gray[center[0],:])
    # plt.show()
    angle = 45
    for i in range(7):
        im_copy = img.copy()
        (h, w) = im_copy.shape[:2]

        M = cv2.getRotationMatrix2D((center[0], center[1]), -angle, 1.0)
        im_copy = cv2.warpAffine(im_copy, M, (w, h))

        contour_rotated = rotate_contour(contours, angle, center)
        cv2.drawContours(im_copy, [contour_rotated], 0, (0, 255, 250), 1)
        preprocessing.show_image("Rotate {}".format(angle), im_copy)  
        angle += 45
    return B