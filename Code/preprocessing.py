import assymetry
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

gaussian_blur_kernel = (29,29)
kernel_for_closing = (29, 29)

dir_out = 'C:/Users/alepa/Desktop/Inz/Out_files/'

# Functions
def read_image(path):
	img = cv2.imread(path)
	return img

def show_image(text, img):
	cv2.imshow(text, img)
	cv2.waitKey(0)

def show_image_TESTING(img):
	cv2.imshow("Test", img)
	cv2.waitKey(0)
	exit(1)

def save_img(text, img):
	cv2.imwrite(text, img)

def convert_to_grayscale(img):
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	return img_gray

def gaussian_blur(img):
	gauss_img = cv2.GaussianBlur(img, gaussian_blur_kernel, cv2.BORDER_DEFAULT) 
	return gauss_img

def apply_otsu_threshold(img):
	otsu_threshold, img_thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
	return otsu_threshold, img_thresh

def morph_closing(img):
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_for_closing)
	img_closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
	return img_closing

def find_contours(img):
	# cnts, hier = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts, hier = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	return cnts, hier

def find_line(contour):
	line_len = 0
	for pixel1, pixel2 in itertools.combinations(contour, 2):
		line_len_temp = math.dist(pixel1[0], pixel2[0])
		if line_len_temp > line_len:
			line_len = line_len_temp
			line_pixel1 = pixel1
			line_pixel2 = pixel2
	return line_pixel1, line_pixel2

def find_line_center(contour, center):
	line_len = 0
	for pixel in contour:
		line_len_temp = math.dist(center, pixel[0])
		if line_len_temp > line_len:
			line_len = line_len_temp
			line_pixel_center = pixel
	return line_pixel_center

def bounding_box(contours, img, original_img):
	max_contour = max(contours, key = cv2.contourArea)
	cv2.drawContours(original_img, max_contour, -1, (0,255,0), 2)
	x,y,w,h = cv2.boundingRect(max_contour)
	rectangle_coordinates = x,y,w,h
	cv2.rectangle(img, (x-offset_minus, y-offset_minus), (x + w + offset_plus, y + h + offset_plus), (0,255,0), 2)

	# [center_x, center_y] = assymetry.find_center(max_contour)
	# center = [center_x, center_y]

	# x_pixel1, x_pixel2 = find_line(max_contour)
	# original_img = cv2.line(original_img, x_pixel1[0], x_pixel2[0], (0, 255, 0), 2)

	# x_pixel = find_line_center(max_contour, center)
	# original_img = cv2.line(original_img, x_pixel[0], center, (0, 255, 0), 2)

	ROI_img = original_img[y-offset_minus:y-offset_minus+h+offset_plus, x-offset_minus:x-offset_minus+w+offset_plus]
	return ROI_img, max_contour, rectangle_coordinates

def main_preprocessing(full_path):
	# try:
		# Close all windows from previous loop
		cv2.destroyAllWindows()

		# Read image
		# full_path = dir+filename
		img = read_image(full_path)

		# Log
		print("[INFO] Processing " + full_path)

		# Copy image
		original_img = img.copy()

		# Convert image to grayscale
		img_gray = convert_to_grayscale(img)

		# Gaussian Blur - the bigger the kernel is the smoother the threshold is
		gauss_img = gaussian_blur(img_gray)

		# OTSU threshold
		otsu_threshold, img_thresh = apply_otsu_threshold(gauss_img)

		# MORPHOLOGY
		# Closing - Dilation continued by erosion
		# construct a rectangular kernel form the current size and apply a "closing" operation
		img_closing = morph_closing(img_thresh)

		# Find contours
		contours, hier = find_contours(img_closing)
		# Obtain bounding box, extract and save ROI
		if len(contours) > 0:
			ROI_img, max_contour, rectangle_coordinates = bounding_box(contours, img_closing, img)
		else:
			print("[INFO] No contours found")

		save_img(dir_out+"1 Original.jpg", original_img)
		save_img(dir_out+"2 Gray.jpg", img_gray)
		save_img(dir_out+"3 Gauss.jpg", gauss_img)
		save_img(dir_out+"4 Threshold.jpg", img_thresh)
		save_img(dir_out+"5 Closing img.jpg", img_closing)
		save_img(dir_out+"6 ROI img.jpg", ROI_img)

		#Log
		print("[INFO] File " + full_path + " processed successfully...\n")

		img_closing = img_closing[rectangle_coordinates[1]-offset_minus:rectangle_coordinates[1]-offset_minus+rectangle_coordinates[3]+offset_plus, rectangle_coordinates[0]-offset_minus:rectangle_coordinates[0]-offset_minus+rectangle_coordinates[2]+offset_plus]
		contours, hier = find_contours(img_closing)
		max_contour = max(contours, key = cv2.contourArea)

		return original_img, img_gray, gauss_img, img_thresh, img_closing, ROI_img, max_contour, rectangle_coordinates
	# except:
	# 	print("[ERROR] Something went wrong for "+full_path)
	
