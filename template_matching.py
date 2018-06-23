import cv2
from os.path import dirname, join, realpath
import os, shutil

import imutils
from imutils.perspective import four_point_transform
from np.magic import np

from templateProcessing import template_image
CHECK =join(dirname(realpath(__file__)), 'static/check/')

FIND_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
RESULT = join(dirname(realpath(__file__)), 'static/output/')
PROCESSED = join(dirname(realpath(__file__)), 'static/processed/')



def templateMatch(filename, filenames):
    print filenames
    image = cv2.imread(PROCESSED + filenames)
    image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)

    # load the image, convert it to grayscale, blur it
    # slightly, then find edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 10)
    edged = cv2.Canny(gray, 50, 200)

    # find contours in the edge map, then initialize
    # the contour that corresponds to the document
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    docCnt = None
    # cv2.imshow('edge', edged)
    # cv2.imshow('blurr', gray)

    # ensure that at least one contour was found
    if len(cnts) > 0:
        # sort the contours according to their size in
        # descending order
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        # loop over the sorted contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # if our approximated contour has four points,
            # then we can assume we have found the paper
            if len(approx) == 4:
                docCnt = approx
                break

    # apply a four point perspective transform to both the
    # original image and grayscale image to obtain a top-down
    # birds eye view of the paper
    paper = four_point_transform(image, docCnt.reshape(4, 2))
    warped = four_point_transform(gray, docCnt.reshape(4, 2))
    blurred = cv2.GaussianBlur(warped, (5, 5), 6)


    # apply Otsu's thresholding method to binarize the warped
    # piece of paper
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 151, 50)

    img = 255 - thresh
    # cv2.imshow('thresholded', img)
    med = cv2.medianBlur(img, 11)
    med = cv2.resize(med, (512, 512))

    ans = cv2.imread(FIND_FOLDER + filename)
    ans = cv2.resize(ans, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    gray1 = cv2.cvtColor(ans, cv2.COLOR_BGR2GRAY)
    edged1 = cv2.Canny(gray1, 50, 200)

    # find contours in the edge map, then initialize
    # the contour that corresponds to the document
    cnts1 = cv2.findContours(edged1.copy(), cv2.RETR_EXTERNAL,
                             cv2.CHAIN_APPROX_SIMPLE)
    cnts1 = cnts1[0] if imutils.is_cv2() else cnts1[1]
    docCnt1 = None
    # cv2.imshow('edge', edged1)

    # ensure that at least one contour was found
    if len(cnts1) > 0:
        # sort the contours according to their size in
        # descending order
        cnts1 = sorted(cnts1, key=cv2.contourArea, reverse=True)

        # loop over the sorted contours
        for c1 in cnts1:
            # approximate the contour
            peri1 = cv2.arcLength(c1, True)
            approx1 = cv2.approxPolyDP(c1, 0.02 * peri1, True)

            # if our approximated contour has four points,
            # then we can assume we have found the paper
            if len(approx1) == 4:
                docCnt1 = approx1
                break

    # apply a four point perspective transform to both the
    # original image and grayscale image to obtain a top-down
    # birds eye view of the paper

    ans = four_point_transform(ans, docCnt1.reshape(4, 2))
    warped1 = four_point_transform(gray1, docCnt1.reshape(4, 2))
    blurred1 = cv2.GaussianBlur(warped1, (5, 5), 6)

    # apply Otsu's thresholding method to binarize the warped
    # piece of paper
    thresh1 = cv2.adaptiveThreshold(blurred1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 151, 90)
    img1 = 255 - thresh1
    # cv2.imshow('thresholded', img1)
    med1 = cv2.medianBlur(img1, 9)
    # final = cv2.GaussianBlur(med, (5, 5), 0)

    # cv2.imshow('Answer', ans)
    # cv2.imshow('Answer processing', med1)
    # med = cv2.resize(med, (512, 512))

    # med = np.asfarray(med)
    med1 = cv2.resize(med1, (512, 512))
    ans = cv2.resize(ans, (512, 512))
    cv2.imwrite(CHECK+filename,med1)
    # cv2.imshow('med1', med1)


    mask = cv2.bitwise_and(med, med1)
    el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    e = cv2.erode(mask, el, iterations=2)
    d = cv2.dilate(e, el, iterations=3)

    im, contours, hierarchy = cv2.findContours(
        d,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    centers = []
    radii = []
    for contour in contours:
        br = cv2.boundingRect(contour)

        m = cv2.moments(contour)
        center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
        centers.append(center)

    print("Total correct answers: {} ".format(len(centers)))

    cnts2 = cv2.findContours(d.copy(), cv2.RETR_EXTERNAL,
                             cv2.CHAIN_APPROX_SIMPLE)
    for c2 in cnts2:
        cv2.drawContours(ans, contours, -1, (0, 255, 0), 3)

    # cv2.imshow('result.png', d)
    cv2.putText(ans, "Correct:" + format(len(centers)), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    cv2.imwrite(RESULT + filename, ans)
    for the_file in os.listdir(PROCESSED):
        file_path = os.path.join(PROCESSED, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    cv2.waitKey(0)