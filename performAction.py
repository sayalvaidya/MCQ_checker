import random
from StdSuites import rows
from os.path import join, dirname, realpath

import cv2
import np
from clint.textui import cols
from pip._internal.cmdoptions import src
from scipy.fftpack import dst

from characterToCsv import character_to_csv
from digitRecognition import recognize_single_character
from processImage import apply_threshold, CV_8UC1
from segmentImage import capture_each_segment, capture_each_character

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
RESULT = join(dirname(realpath(__file__)), 'static/output/')
UPLOAD_FOLDER_CURRENT = join(dirname(realpath(__file__)), 'static/processedImages/')
temp={}
def alpha_dict(ans_set):
   global temp
   temp= ans_set

def image_processing(filename):

    # img = cv2.imread(UPLOAD_FOLDER+filename)
    filename_new = apply_threshold(filename)
    segments_contours_img = capture_each_segment(filename_new, filename_new)
    # blurred_img = cv2.medianBlur(img, 5)
    # img_grey = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)
    #
    #
    # cv2.imwrite(UPLOAD_FOLDER_CURRENT + "Image1_" + str(random.randint(1, 100000)) + "_MedianBlurred.png", blurred_img)
    # th_img = cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 151, 18)
    # # th_img= cv2.threshold(img_grey, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    # inverted_img = 255 - th_img
    # cv2.imwrite(UPLOAD_FOLDER_CURRENT + 'Image2_' + str(random.randint(1, 100000)) + '_InvertedImage.png', inverted_img)
    # inverted_blurred_img = cv2.medianBlur(inverted_img, 5)
    # img_name = 'Image3_' + str(random.randint(1, 100000)) + '_InvertedMedianBlurredImage.png'
    # cv2.imwrite(UPLOAD_FOLDER_CURRENT + img_name, inverted_blurred_img)
    # segments_contours_img = capture_each_segment(img_name, img_name)
    print(segments_contours_img)
    i = 0
    characters_img = []
    for segment in segments_contours_img:
        each_character_img = capture_each_character(segment, segment, i)
        characters_img.append(each_character_img)
        i += 1
    print(characters_img)
    return characters_img


def recognition_character(characters_img):
    # image = cv2.imread(UPLOAD_FOLDER + filename)
    # image = cv2.resize(image,(512,512))

    global temp
    recognized_characters_list = []
    for each_segment_img_list in characters_img:
        segment_characters = []
        for each_character_img in each_segment_img_list:
            character_csv = character_to_csv(each_character_img)
            recognized_character = recognize_single_character(character_csv)
            print("Recognized Character is ", recognized_character)
            recognized_characters_list.append(recognized_character)
    print("Recognized Characters List is ", recognized_characters_list)
    ans_set = {}
    i = 0
    while (i < len(recognized_characters_list)):
        if recognized_characters_list[i] == '1' or recognized_characters_list[i] == '2' or recognized_characters_list[i] == '3' or recognized_characters_list[i] == '4' or \
                        recognized_characters_list[i] == '5' or recognized_characters_list[i] == '6' or recognized_characters_list[i] == '7' or recognized_characters_list[
            i] == '8' or recognized_characters_list[i] == '9' or recognized_characters_list[i] == '0':
            n = recognized_characters_list[i]
            n = int(str(n))
            if recognized_characters_list[i + 1] == '0' or recognized_characters_list[i + 1] == '1' or recognized_characters_list[i + 1] == '2' or recognized_characters_list[
                        i + 1] == '3' or recognized_characters_list[i + 1] == '4' or recognized_characters_list[i + 1] == '5' or recognized_characters_list[
                        i + 1] == '6' or recognized_characters_list[i + 1] == '7' or recognized_characters_list[i + 1] == '8' or recognized_characters_list[
                        i + 1] == '9':
                n = n * 10 + int(str(recognized_characters_list[i + 1]))
                if recognized_characters_list[i + 2] == 'A' or recognized_characters_list[i + 2] == 'B' or recognized_characters_list[i + 2] == 'C' or recognized_characters_list[
                            i + 2] == 'D' or recognized_characters_list[i + 2] == '%':
                    ans_set[n] = recognized_characters_list[i + 2]
                    i = i + 3
                else:
                    print "error"
                    break
            else:
                ans_set[n] = recognized_characters_list[i + 1]
                i = i + 2
        else:
            print "error"
            break
        print i
    print ans_set
    correct = 0
    for k in ans_set:
        if ans_set[k] == temp[k]:
            correct = correct + 1

    print correct

    return correct


