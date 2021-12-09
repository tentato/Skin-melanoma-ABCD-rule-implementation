import preprocessing
import assymetry
import border
import color
import sys
import time
import os

open('C:/Users/alepa/Desktop/Inz/Code/log_file.txt', 'w').close()
log_file = open("C:/Users/alepa/Desktop/Inz/Code/log_file.txt", "a")

path = 'C:/Users/alepa/Desktop/Inz/Skin_melanoma/to_process/'

# full_path = sys.argv[1]

A = 0.0
B = 0.0
C = 0.0

#############################
#####	Main function	#####
#############################

if __name__=="__main__":
    start = time.time()
    for file in os.listdir(path):
        full_path = path + file
        original_img, img_gray, gauss_img, img_thresh, img_closing, ROI_img, max_contour, rectangle_coordinates = preprocessing.main_preprocessing(full_path, log_file)
        center = preprocessing.find_center(max_contour)
        A = assymetry.main_assymetry(max_contour, center, log_file, original_img)
        # B = border.main_border(original_img, center, max_contour, log_file)
        # C = color.main_color(original_img, max_contour, log_file)
        end = time.time()

        print("[Wyniki] Analiza zakończona w czasie ", round(end-start, 2), " sekund")
        print("[Wyniki] A=", round(A, 1))
        print("[Wyniki] B=", round(B, 1))
        print("[Wyniki] C=", round(C, 1))
        print("")
        log_file.write("[Wyniki] Analiza zakończona w czasie {} sekund\n".format(round(end-start, 2)))
        log_file.write("[Wyniki] A={}\n".format(round(A, 1)))
        log_file.write("[Wyniki] B={}\n".format(round(B, 1)))
        log_file.write("[Wyniki] C={}\n".format(round(C, 1)))

        log_file.close()

        sys.exit()