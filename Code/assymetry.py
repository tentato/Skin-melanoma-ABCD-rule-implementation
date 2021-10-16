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


offset_minus = 50
offset_plus = offset_minus*2

def find_center(contour):
	Moment = cv2.moments(contour)
	centerX = int(Moment["m10"] / Moment["m00"])
	centerY = int(Moment["m01"] / Moment["m00"])
	return [centerX, centerY]

def find_vertical_line(contour, center):
	x = center[0]
	# vertical_pixel = 0
	# for p in contour:
	# 	px = p[0][0]
	# 	if px == x:
	# 		vertical_pixel = p[0]	
	return x

def find_line(contour, center):
	p1 = center
	p2 = contour[2][0]
	a = (p1[1]-p2[1])/(p1[0]-p2[0]) 	# a = y1 - y2 / x1 - x2
	b = p1[1] - a * p1[0] 				# b = y - ax	
	return a, b

def find_random_contour_pixel(contour):
	rand_i = randrange(len(contour))
	rand_pixel = contour[rand_i][0]
	return rand_pixel

def find_perpendicular_line(a, b, pixel):
	a = 0 								# horizontal line, a=0
	# a = -1 / a
	b = pixel[1] - a * pixel[0]
	return a, b

def find_second_pixel(a, b, pixel, contour):
	second_pixel = [0, 0]
	for p in contour:		
		x = p[0][0]
		y = p[0][1]
		val = a * x + b - y
		if val == 0:
			print(p[0])
	print("\n")
	# print(pixel)
	# print(second_pixel)
	return second_pixel

def find_second_horizontal_pixel(pixel, contour):
	x = pixel[0]
	y = pixel[1]
	for p in contour:
		px = p[0][0]
		py = p[0][1]
		if py == y:
			if px != x:
				second_horizontal_pixel = p[0]	
	return second_horizontal_pixel

#####	Main function	#####

def main_assymetry(contour):
	center_X, center_Y = find_center(contour)
	center = center_X, center_Y
	print("Center:")
	print(center)
	x_vertical_line = find_vertical_line(contour, center)
	# a, b = find_line(contour, center)
	print("Vertical line:")
	print(x_vertical_line)
	random_pixel = find_random_contour_pixel(contour)
	print("Random pixel:")
	print(random_pixel)
	second_horizontal_pixel = find_second_horizontal_pixel(random_pixel, contour)
	print("Second horizontal pixel:")
	print(second_horizontal_pixel)


	# perpendicular_a, perpendicular_b = find_perpendicular_line(a, b, random_pixel)
	# print(perpendicular_a)
	# print(perpendicular_b)
	# second_pixel = find_second_pixel(perpendicular_a, perpendicular_b, random_pixel, contour)







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


	# do sprawdzenia czy punkty leza na lini
	# if a*p1[0]+b - p1[1] == 0:
	# 	print("p1 nalezy")
	# else:
	# 	print("p1 nie nalezy")

	# if a*p2[0]+b - p2[1] == 0:
	# 	print("p2 nalezy")
	# else:
	# 	print("p2 nie nalezy")