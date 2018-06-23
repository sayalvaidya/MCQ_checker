from os.path import dirname, join, realpath

import cv2
import imutils
from imutils.perspective import four_point_transform

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
TEMPLATE = join(dirname(realpath(__file__)), 'static/template/')
RESULT = join(dirname(realpath(__file__)), 'static/output/')
PROCESSED = join(dirname(realpath(__file__)), 'static/processed/')


def template_image(filename):
    image = cv2.imread(TEMPLATE + filename)
    # image = cv2.resize(image, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_CUBIC)
    #
    # # load the image, convert it to grayscale, blur it
    # # slightly, then find edges
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # blurred = cv2.GaussianBlur(gray, (5, 5), 10)
    # edged = cv2.Canny(gray, 50, 200)
    #
    # # find contours in the edge map, then initialize
    # # the contour that corresponds to the document
    # cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    #                         cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    # docCnt = None
    # # cv2.imshow('edge', edged)
    # # cv2.imshow('blurr', gray)
    #
    # # ensure that at least one contour was found
    # if len(cnts) > 0:
    #     # sort the contours according to their size in
    #     # descending order
    #     cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    #
    #     # loop over the sorted contours
    #     for c in cnts:
    #         # approximate the contour
    #         peri = cv2.arcLength(c, True)
    #         approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    #
    #         # if our approximated contour has four points,
    #         # then we can assume we have found the paper
    #         if len(approx) == 4:
    #             docCnt = approx
    #             break
    #
    # # apply a four point perspective transform to both the
    # # original image and grayscale image to obtain a top-down
    # # birds eye view of the paper
    # paper = four_point_transform(image, docCnt.reshape(4, 2))
    # warped = four_point_transform(gray, docCnt.reshape(4, 2))
    # blurred = cv2.GaussianBlur(warped, (5, 5), 6)
    #
    # # apply Otsu's thresholding method to binarize the warped
    # # piece of paper
    # thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 151, 50)
    # img = 255 - thresh
    # # cv2.imshow('thresholded', img)
    # med = cv2.medianBlur(img, 11)
    # med = cv2.resize(med, (512, 512))
    # final = cv2.GaussianBlur(med, (5, 5), 0)

    # cv2.imshow('Template', paper)
    # cv2.imshow('Template processing', med)
    cv2.imwrite(PROCESSED + filename, image)
