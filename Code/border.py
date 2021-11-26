import preprocessing
import cv2

def find_top_pixel(contour, center):
    x = center[0]
    current_min = 1000000
    for p in contour:
        px = p[0][0]
        py = p[0][1]
        if px == x:
            if py < current_min:
                current_min = py
    top_pixel = [x, current_min]
    return top_pixel

def find_avg_out(pixel, img, pixels_used):
    img_copy = img.copy()
    sum = 0
    count = 5
    for i in range(int(pixels_used)):
        try:    # in case not enough pixels out of the contour
            sum += img_copy[pixel[1]-count, pixel[0]]
            count += 1
        except:
            break
    avg_out = sum / count
    return avg_out

def find_avg_in(pixel, center, img):
    img_copy = img.copy()
    sum = 0
    count = 0
    range_pixels = (center[1] - pixel[1]) / 10

     # checks all pixels between top pixel and center to get better average
    for i in range(int(range_pixels)):
        sum += img_copy[pixel[1]+count, pixel[0]]
        count += 1
    avg_in = sum / count
    return avg_in, range_pixels

def check_border_sharp(avg_in, avg_out):
    difference = avg_out - avg_in
    if difference > 100:
        b = 0.0
    else:
        b = 1.0
    return b

#############################
#####	Main function	#####
#############################

def main_border(img, center, contours, log):
    try:
        B = 0.0
        b = 0.0
        b_temp = 0.0
        log.write("[INFO] BORDER ANALYZING STARTED\n")
        print("[INFO] BORDER ANALYZING STARTED")
        angle = 45
        for i in range(8):
            # log.write("[INFO] Border analyzing for angle = {}\n".format(angle))
            # print("[INFO] Border analyzing for angle = ", angle)
            im_copy = img.copy()
            (h, w) = im_copy.shape[:2]

            M = cv2.getRotationMatrix2D((center[0], center[1]), -angle, 1.0)
            im_copy = cv2.warpAffine(im_copy, M, (w, h))

            contour_rotated = preprocessing.rotate_contour(contours, angle, center)
            top_pixel = find_top_pixel(contour_rotated, center)
            im_copy = preprocessing.convert_to_grayscale(im_copy)
            im_copy = preprocessing.gaussian_blur(im_copy)

            # close to 0 - darker, close to 255 - lighter
            avg_in, pixels_used = find_avg_in(top_pixel, center, im_copy)
            avg_out = find_avg_out(top_pixel, im_copy, pixels_used)
            
            cv2.drawContours(im_copy, [contour_rotated], 0, (0, 255, 250), 1)
            # cv2.circle(im_copy, top_pixel, 3, (0, 255, 0), -1)
            # cv2.circle(im_copy, center, 3, (0, 255, 0), -1)
            preprocessing.show_image("Rotate {}".format(angle), im_copy)
            b_temp = check_border_sharp(avg_in, avg_out)
            b += b_temp
            angle += 45
        
        log.write("[INFO] Blured border section: {} / 8\n".format(int(8 - b)))
        print("[INFO] Blured border section: ", int(8 - b), "/ 8")

        B = b * 0.1
        log.write("[INFO] B after all checks: {}\n".format(B))
        print("[INFO] B after all checks: ", B)

        log.write("[INFO] Border analyzing finished\n\n")
        print("[INFO] Border analyzing finished\n")
        return B
    except:
	    log.write("[ERROR] Unhandled border analyzing error - something went wrong\n")
	    print("[ERROR] Unhandled border analyzing error - something went wrong")