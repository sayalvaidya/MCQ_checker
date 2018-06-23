import random

import cv2
from cv2 import *
from os.path import join, dirname, realpath

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/processedImages/')
FOLDER_SEGMENTED_IMAGES = join(dirname(realpath(__file__)), 'static/segmentedImages/')
FOLDER_DIGIT_SEGMENTED_IMAGES = join(dirname(realpath(__file__)), 'static/digitSegmentedImages/')


def capture_each_segment(filename, filename_uc):
    img = cv2.imread(UPLOAD_FOLDER + filename)
    uc_img = cv2.imread(UPLOAD_FOLDER + filename_uc)
    gray_scale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray_scale_img, 180, 255, cv2.THRESH_BINARY)
    final_img = cv2.bitwise_and(gray_scale_img, gray_scale_img, mask=mask)
    ret, new_img = cv2.threshold(final_img, 180, 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (9,
                                                         1))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
    dilated_img = cv2.dilate(new_img, kernel, iterations=50)  # dilate , more the iteration more the dilation
    image, contours, hierarchy = cv2.findContours(dilated_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours_img = []
    for contour in contours:
        [x, y, w, h] = cv2.boundingRect(contour)
        contours_img.append([x, y, w, h])

    contours_img.sort(key=lambda x: x[1])

    i = 0
    segment_img = []
    for contour in contours_img:
        # get rectangle bounding contour
        [x, y, w, h] = contour
        # eliminating false positive from our contour
        if w < 20 and h < 20:
            continue

        # drawing rectangle around contour
        rec_img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
        cv2.imwrite(str(FOLDER_SEGMENTED_IMAGES) + "Image1_" + str(i) + "_" + str(
            random.randint(1, 100000)) + "_SegmentedImage.png", rec_img)

        # crop each contour and save individually
        cropped_img = final_img[y:y + h, x:x + w]

        each_contour_img = 'Image2_' + str(i) + '_' + str(random.randint(1, 100000)) + '_segmentedContour' + str(
            i) + '.png'
        cv2.imwrite(str(FOLDER_SEGMENTED_IMAGES) + each_contour_img, cropped_img)
        i += 1
        segment_img.append(each_contour_img)
    return segment_img


def capture_each_character(filename, filename_uc, cii):
    img = cv2.imread(FOLDER_SEGMENTED_IMAGES + filename)
    uc_img = cv2.imread(FOLDER_SEGMENTED_IMAGES + filename_uc)
    gray_scale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray_scale_img, 180, 255, cv2.THRESH_BINARY)
    final_img = cv2.bitwise_and(gray_scale_img, gray_scale_img, mask=mask)
    ret, new_img = cv2.threshold(final_img, 180, 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (1,
                                                         1))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
    dilated_img = cv2.dilate(new_img, kernel, iterations=1)  # dilate , more the iteration more the dilation

    # cv2.imwrite(FOLDER_SEGMENTED_IMAGES + "finalDilatedImage.png", dilated_img)

    image, contours, hierarchy = cv2.findContours(dilated_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours_img = []
    for contour in contours:
        [x, y, w, h] = cv2.boundingRect(contour)
        contours_img.append([x, y, w, h])

    contours_img.sort()

    i = 0
    digit_segment_img = []
    digit_segmented_img_name = "Image3_" + str(cii) + "_" + str(
            random.randint(1, 100000)) + "_digitSegmentedImage.png"
    for contour in contours_img:
        # get rectangle bounding contour
        [x, y, w, h] = contour
        # eliminating false positive from our contour
        if w < 20 and h < 20:
            continue

        # drawing rectangle around contour
        rec_img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
        cv2.imwrite(str(FOLDER_SEGMENTED_IMAGES) + digit_segmented_img_name, rec_img)

        # crop each contour and save individually
        cropped_img = final_img[y:y + h, x:x + w]
        if i > 9:
            if i > 19:
                name_char = 'c'
            else:
                name_char = 'b'
        else:
            name_char = 'a'
        each_digit_contour_img = 'segmentedDigitContour_' + str(cii) + '_' + name_char + str(i) + '_' + str(
            random.randint(1, 100000)) + '.png'
        cv2.imwrite(str(FOLDER_DIGIT_SEGMENTED_IMAGES) + each_digit_contour_img, cropped_img)
        i += 1
        digit_segment_img.append(each_digit_contour_img)
    return digit_segment_img
