import random
from os.path import join, dirname, realpath
import cv2
from cv2 import *

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
UPLOAD_FOLDER_CURRENT = join(dirname(realpath(__file__)), 'static/processedImages/')


def apply_threshold(filename):
    img = cv2.imread(UPLOAD_FOLDER + filename, 0)
    # cv2.imshow("Image after read",img)
    # cv2.waitKey(5000)
    blurred_img = cv2.medianBlur(img, 5)
    cv2.imwrite(UPLOAD_FOLDER_CURRENT + "Image1_" + str(random.randint(1, 100000)) + "_MedianBlurred.png", blurred_img)
    th_img = cv2.adaptiveThreshold(blurred_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 151, 18)
    inverted_img = 255 - th_img
    cv2.imwrite(UPLOAD_FOLDER_CURRENT + 'Image2_' + str(random.randint(1, 100000)) + '_InvertedImage.png', inverted_img)
    inverted_blurred_img = cv2.medianBlur(inverted_img, 5)
    img_name = 'Image3_'+str(random.randint(1,100000))+'_InvertedMedianBlurredImage.png'
    cv2.imwrite(UPLOAD_FOLDER_CURRENT + img_name, inverted_blurred_img)
    return img_name
