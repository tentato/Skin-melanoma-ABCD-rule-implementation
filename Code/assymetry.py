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

def find_vertical_line(center):
	x = center[0]
	return x

def find_horizontal_line(center):
	y = center[1]
	return y

def find_extreme_vertical_pixels(x_vertical, contour):
	y = 100000
	for p in contour:
		px = p[0][0]
		py = p[0][1]
		if px == x_vertical:
			if py < y:
				y = py
				min_y_pixel = p[0]

	for p in contour:
		px = p[0][0]
		py = p[0][1]
		if px == x_vertical:
			if py > y:
				y = py
				max_y_pixel = p[0]
	return min_y_pixel, max_y_pixel

def find_extreme_horizontal_pixels(y_horizontal, contour):
	x = 100000
	for p in contour:
		px = p[0][0]
		py = p[0][1]
		if py == y_horizontal:
			if px < x:
				x = px
				min_x_pixel = p[0]

	for p in contour:
		px = p[0][0]
		py = p[0][1]
		if py == y_horizontal:
			if px > x:
				x = px
				max_x_pixel = p[0]
	return min_x_pixel, max_x_pixel	

def find_next_line_point(current, max):
	temp_current = current + 5
	if temp_current < max:
		current += 5

	if temp_current + 5 > max:
		next_loop_possible = False
	else:
		next_loop_possible = True
	return current, next_loop_possible

def find_min_for_current(current, contour):
	min = 100000
	for p in contour:
		px = p[0][0]
		py = p[0][1]
		if py == current:
			if px < min:
				min = px		
	return min

def find_max_for_current(current, contour):
	max = 0
	for p in contour:
		px = p[0][0]
		py = p[0][1]
		if py == current:
			if px > max:
				max = px		
	return max

def find_length_ratio(x, pixel1, pixel2):
	p1_x = pixel1[0]
	p2_x = pixel2[0]
	length1 = abs(p1_x - x)
	length2 = abs(p2_x - x)
	if length1 > length2:
		ratio = length2 / length1
	else:
		ratio = length1 / length2
	return ratio

def analyze_ratio_array(ratio_array):
	count = 0
	for ratio in ratio_array:
		if ratio > 0.75:
			count += 1
	
	if count > len(ratio_array)*0.75:	
		A = 1
	else:
		A = 0
	return A

#############################
#####	Main function	#####
#############################

def main_assymetry(contour, center):
	A = 2

	print("[INFO] Center: ", center)

	x_vertical_line = find_vertical_line(center)
	print("[INFO] Vertical line: ", x_vertical_line)
	y_horizontal_line = find_horizontal_line(center)
	print("[INFO] Horizontal line: ", y_horizontal_line)

	### Vertical

	min_y_pixel, max_y_pixel = find_extreme_vertical_pixels(x_vertical_line, contour)	
	print("[INFO] min y, max y: ", min_y_pixel[1], max_y_pixel[1])
	current_y = min_y_pixel[1]

	next_loop_possible = True
	ratio_array = []
	while(next_loop_possible):
		print("[INFO] Current Y: ", current_y)
		current_y, next_loop_possible = find_next_line_point(current_y, max_y_pixel[1])
		print("[INFO] Current Y - next: ", current_y)
		next_pixel = [find_min_for_current(current_y, contour), current_y]
		print("[INFO] Next pixel: ", next_pixel)

		second_horizontal_pixel = [find_max_for_current(current_y, contour), current_y]
		print("[INFO] Second horizontal pixel: ", second_horizontal_pixel)
		ratio = find_length_ratio(x_vertical_line, next_pixel, second_horizontal_pixel)
		print("[INFO] Ratio: ", ratio)
		ratio_array.append(ratio)

	a_vertical = analyze_ratio_array(ratio_array)
	A = A - a_vertical
	print("[INFO] Ma after vertical check: ", A)

	### Horizontal

	min_x_pixel, max_x_pixel = find_extreme_horizontal_pixels(y_horizontal_line, contour)	
	print("[INFO] min x, max x: ", min_x_pixel[1], max_x_pixel[1])
	current_x = min_x_pixel[1]

	next_loop_possible = True
	ratio_array = []
	while(next_loop_possible):
		print("[INFO] Current X: ", current_x)
		current_x, next_loop_possible = find_next_line_point(current_x, max_x_pixel[1])
		print("[INFO] Current X - next: ", current_y)
		next_pixel = [find_min_for_current(current_x, contour), current_x]
		print("[INFO] Next pixel: ", next_pixel)

		second_horizontal_pixel = [find_max_for_current(current_x, contour), current_x]
		print("[INFO] Second horizontal pixel: ", second_horizontal_pixel)
		ratio = find_length_ratio(y_horizontal_line, next_pixel, second_horizontal_pixel)
		print("[INFO] Ratio: ", ratio)
		ratio_array.append(ratio)

	a_horizontal = analyze_ratio_array(ratio_array)
	A = A - a_horizontal
	print("[INFO] Ma after horizontal check: ", A)

	A = A*1.3
	print("[INFO] A after vertical and horizontal check: ", A)

	return A