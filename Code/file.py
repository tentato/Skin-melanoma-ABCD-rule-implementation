import cv2

import numpy as np
import argparse
import time
import os
import itertools
import math

import numpy as np
import matplotlib.pyplot as plt
import scipy.misc

offset_minus = 50
offset_plus = offset_minus*2

gaussian_blur_kernel = (29,29)
kernel_for_closing = (19, 19)

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

def x_axis(contour):
	x_axis_len = 0
	for pixel1, pixel2 in itertools.combinations(contour, 2):
		x_axis_len_temp = math.dist(pixel1[0], pixel2[0])
		if x_axis_len_temp > x_axis_len:
			x_axis_len = x_axis_len_temp
			x_axis_pixel1 = pixel1
			x_axis_pixel2 = pixel2
	return x_axis_pixel1, x_axis_pixel2

def bounding_box(contours, img, original_img):
	max_contour = max(contours, key = cv2.contourArea)
	cv2.drawContours(original_img, max_contour, -1, (0,255,0), 2)
	x,y,w,h = cv2.boundingRect(max_contour)
	rectangle_coordinates = x,y,w,h
	cv2.rectangle(img, (x-offset_minus, y-offset_minus), (x + w + offset_plus, y + h + offset_plus), (0,255,0), 2)

	# x_pixel1, x_pixel2 = x_axis(max_contour)
	# original_img = cv2.line(original_img, x_pixel1[0], x_pixel2[0], (0, 255, 0), 2)

	ROI_img = original_img[y-offset_minus:y-offset_minus+h+offset_plus, x-offset_minus:x-offset_minus+w+offset_plus]
	return ROI_img, max_contour, rectangle_coordinates


dir = 'C:/Users/alepa/Desktop/Inz/Skin melanoma/to process/'
for filename in os.listdir(dir):

	# try:
		# Close all windows from previous loop
		cv2.destroyAllWindows()

		# Read image
		full_path = dir+filename
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
			ROI_img, max_contour, rectangle_coordinates = bounding_box(contours, img_closing, original_img)
		else:
			print("[INFO] No contours found")

		show_image("ROI image", ROI_img)

		#Erosion
		# for i in range(0, 3):
		# 	eroded = cv2.erode(img_thresh, None, iterations=i+1)
		# 	cv2.imshow("Eroded {} times".format(i+1), eroded)
		# 	cv2.waitKey(0)

		#Dilation
		# for i in range(0, 3):	
		# 	dilated = cv2.dilate(img_thresh, None, iterations=i+1)
		# 	cv2.imshow("Dilated {} times".format(i+1), dilated)
		# 	cv2.waitKey(0)

		# exit()

		# # variables for GrabCut algorithm
		# rectangle_coordinates=(x-offset_minus, y-offset_minus, x + w + offset_plus, y + h + offset_plus)
		# fgModel = np.zeros((1, 65), dtype="float")
		# bgModel = np.zeros((1, 65), dtype="float")
		# mask = np.zeros(gauss_img.shape[:2], dtype="uint8")

		# gauss_img_color = cv2.cvtColor(gauss_img, cv2.COLOR_GRAY2BGR)

		# start = time.time()
		# (mask, bgModel, fgModel) = cv2.grabCut(gauss_img_color, mask, rectangle_coordinates, bgModel, fgModel, iterCount=5, mode=cv2.GC_INIT_WITH_RECT)
		# end = time.time()
		# print("[INFO] applying GrabCut took {:.2f} seconds".format(end - start) + " for " + full_path)

		# values = (
		# 	("Definite Background", cv2.GC_BGD),
		# 	("Probable Background", cv2.GC_PR_BGD),
		# 	("Definite Foreground", cv2.GC_FGD),
		# 	("Probable Foreground", cv2.GC_PR_FGD),
		# )
		# # loop over the possible GrabCut mask values
		# for (name, value) in values:
		# 	# construct a mask that for the current value
		# 	# print("[INFO] showing mask for '{}'".format(name))
		# 	valueMask = (mask == value).astype("uint8") * 255
		# 	# # display the mask so we can visualize it
		# 	# cv2.imshow(name, valueMask)
		# 	# cv2.waitKey(0)

		# # we'll set all definite background and probable background pixels
		# # to 0 while definite foreground and probable foreground pixels are
		# # set to 1
		# outputMask = np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD), 0, 1)
		# # scale the mask from the range [0, 1] to [0, 255]
		# outputMask = (outputMask * 255).astype("uint8")
		# # apply a bitwise AND to the image using our mask generated by
		# # GrabCut to generate our final output image
		# output = cv2.bitwise_and(gauss_img, gauss_img, mask=outputMask)
		# output = output[y - offset_minus : y - offset_minus + h + offset_plus, x - offset_minus : x - offset_minus + w + offset_plus]


		# # show the input image followed by the mask and output generated by
		# # GrabCut and bitwise masking
		# # cv2.imshow("Input", gauss_img)
		# # cv2.imshow("GrabCut Mask", outputMask)
		# cv2.imshow("GrabCut Output", output)
		# cv2.waitKey(0)


		# # Save ROI image
		# cv2.imwrite('test.jpg', ROI)
		# cv2.imwrite('out_melanoma.jpg', output)
		
		#Log
		print("[INFO] File " + full_path + " processed successfully...\n")
	# except:
	# 	print("[ERROR] Something went wrong for "+full_path)
