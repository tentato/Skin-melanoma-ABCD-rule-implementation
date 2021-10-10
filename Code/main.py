import preprocessing
import assymetry

import cv2

# A, B, C, D = 0

if __name__=="__main__":
    original_img, img_gray, gauss_img, img_thresh, img_closing, ROI_img, max_contour, rectangle_coordinates = preprocessing.main_preprocessing()

    # A = assymetry.main()

    cx, cy = preprocessing.find_center(max_contour)
    cv2.circle(ROI_img, (cx, cy), 7, (0, 255, 0), -1)
    cv2.circle(original_img, (cx, cy), 7, (0, 255, 0), -1)

    preprocessing.show_image("test1", ROI_img)
    preprocessing.show_image("test2", original_img)
