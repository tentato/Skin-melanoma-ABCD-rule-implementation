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

def find_center(contour):
	Moment = cv2.moments(contour)
	centerX = int(Moment["m10"] / Moment["m00"])
	centerY = int(Moment["m01"] / Moment["m00"])
	return centerX, centerY

# 1. Find vertical line containing center, function: Ax + By + C = 0, B=0, 
# 2. 
# 3.
# 4.
# 5.
# 6.
# 7.
# 8.
# 9.





































# def find_bounding_square_ROI(img, rect_coordinates):
#     x, y, w, h = rect_coordinates
#     width = math.dist((x, y), (w, y))
#     height = math.dist((x, y), (x, h))

#     print(width)
#     print(height)

#     if width > height:
#         delta = width - height
#         centered_square_ROI = img[ int(y-delta/2) : int(y-delta/2) + int(h-delta/2), x : x + w]
#     elif width < height:
#         delta = height - width
#         print(delta)
#         # centered_square_ROI = img[ y : y + h, x : x + w]
#         centered_square_ROI = img[ y : y + h, x + int(delta/2) : x + int(delta/2) + w - int(delta/2)]
#     else:
#         centered_square_ROI = img

#     out_dim = centered_square_ROI.shape
#     print("Out shape")
#     print(out_dim[0])
#     print(out_dim[1])
#     return centered_square_ROI