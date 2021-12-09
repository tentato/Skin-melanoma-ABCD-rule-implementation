import cv2
import math
import preprocessing

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

def find_min_for_current_X(current, contour):
	min = 100000
	for p in contour:
		px = p[0][0]
		py = p[0][1]
		if px == current:
			if py < min:
				min = py		
	return min

def find_max_for_current_X(current, contour):
	max = 0
	for p in contour:
		px = p[0][0]
		py = p[0][1]
		if px == current:
			if py > max:
				max = py		
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

def find_max_distance(cnt):
	max_dist = 0

	for p1 in cnt:
		for p2 in cnt:
			dist = math.sqrt( (p2[0][0] - p1[0][0])**2 + (p2[0][1] - p1[0][1])**2 )
			if dist > max_dist:
				max_dist = dist
				pixel1 = p1[0]
				pixel2 = p2[0]

	return pixel1, pixel2

def analyze_ratio_array(ratio_array):
	count = 0
	for ratio in ratio_array:
		if ratio > 0.80:
			count += 1
	
	if count >= len(ratio_array)*0.80:	
		A = 1
	else:
		A = 0
	return A

#############################
#####	Main function	#####
#############################

def main_assymetry(contour, center, log, imgTBD):
	try:
		A = 2

		log.write("[INFO] ANALIZA ASYMETRII ROZPOCZĘTA\n")
		print("[INFO] ANALIZA ASYMETRII ROZPOCZĘTA")

		### Peparing 
		x_vertical_line = find_vertical_line(center)
		y_horizontal_line = find_horizontal_line(center)

		### Rotating image
		copy_contour = contour.copy()

		pixel1, pixel2 = find_max_distance(copy_contour)
		a = ((pixel1[1]*-1)-(pixel2[1]*-1))/(pixel1[0]-pixel2[0])
		alpha = math.atan(a)
		alpha = alpha * 57.3 # radiany na stopnie

		if alpha < 90:
			alpha = 90 - alpha
			copy_contour = preprocessing.rotate_contour(copy_contour, -alpha, center)
		else:
			alpha = alpha - 90
			copy_contour = preprocessing.rotate_contour(copy_contour, alpha, center)

		# cv2.drawContours(imgTBD, [copy_contour], 0, (0, 255, 250), 1)
		# preprocessing.show_image("Rotate ", imgTBD)

		### Vertical symetry check
		min_y_pixel, max_y_pixel = find_extreme_vertical_pixels(x_vertical_line, copy_contour)	
		current_y = min_y_pixel[1]

		next_loop_possible = True
		ratio_array = []
		while(next_loop_possible):
			current_y, next_loop_possible = find_next_line_point(current_y, max_y_pixel[1])

			next_pixel = [find_min_for_current(current_y, copy_contour), current_y]

			second_horizontal_pixel = [find_max_for_current(current_y, copy_contour), current_y]

			ratio = find_length_ratio(x_vertical_line, next_pixel, second_horizontal_pixel)
			ratio_array.append(ratio)


		a_vertical = analyze_ratio_array(ratio_array)
		A = A - a_vertical
		log.write("[INFO] Symmetria wzdłuż dłuższej osi pionowej: {}\n".format(a_vertical))
		print("[INFO] Symmetria wzdłuż osi pionowej: ", a_vertical)


		### Horizontal symetry check
		min_x_pixel, max_x_pixel = find_extreme_horizontal_pixels(y_horizontal_line, copy_contour)	
		current_x = min_x_pixel[0]

		next_loop_possible = True
		ratio_array = []
		while(next_loop_possible):
			current_x, next_loop_possible = find_next_line_point(current_x, max_x_pixel[0])

			next_pixel = [find_min_for_current_X(current_x, copy_contour), current_x]

			second_horizontal_pixel = [find_max_for_current_X(current_x, copy_contour), current_x]

			ratio = find_length_ratio(y_horizontal_line, next_pixel, second_horizontal_pixel)

			ratio_array.append(ratio)

		a_horizontal = analyze_ratio_array(ratio_array)
		log.write("[INFO] Symmetria wzdłuż osi poziomej: {}\n".format(a_horizontal))
		print("[INFO] Symmetria wzdłuż osi poziomej: ", a_horizontal)
		A = A - a_horizontal

		A = A*1.3
		log.write("[INFO] Wartość A po analizie: {}\n".format(A))
		print("[INFO] Wartość A po analizie: ", A)

		log.write("[INFO] Analiza asymetrii zakończona\n\n")
		print("[INFO] Analiza asymetrii zakończona\n")

		return A
	except:
		log.write("[ERROR] Nieoczekiwany błąd analizy asymetrii\n")
		print("[ERROR] Nieoczekiwany błąd analizy asymetrii")