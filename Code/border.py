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

import preprocessing




#############################
#####	Main function	#####
#############################

def main_border(img, center):
    B = 0
    img_gray = preprocessing.convert_to_grayscale(img)
    img_gray = preprocessing.gaussian_blur(img_gray)
    plt.plot(img_gray[center[0],:])
    plt.show()
    return B