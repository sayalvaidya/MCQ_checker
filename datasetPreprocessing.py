import cv2
import os

import imutils

if __name__ == "__main__":
    for filename in os.listdir('./static/dataset'):
        img = cv2.imread('./static/dataset'+filename)
        img = 255 - img
        gray_scale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_scale_img, 180, 255, cv2.THRESH_BINARY)
        final_img = cv2.bitwise_and(gray_scale_img, gray_scale_img, mask=mask)
        ret, new_img = cv2.threshold(final_img, 180, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (1,
                                                             1))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
        dilated_img = cv2.dilate(new_img, kernel, iterations=1)  # dilate , more the iteration more the dilation

        image, contours, hierarchy = cv2.findContours(dilated_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours_img = []
        for contour in contours:
            [x, y, w, h] = cv2.boundingRect(contour)
            contours_img.append([x, y, w, h])

        contours_img.sort()

        i = 0
        digit_segment_img = []

        for contour in contours_img:
            # get rectangle bounding contour
            [x, y, w, h] = contour
            # eliminating false positive from our contour
            if w < 20 and h < 20:
                continue

            # drawing rectangle around contour
            rec_img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

            # crop each contour and save individually
            cropped_img = final_img[y:y + h, x:x + w]
        final_img = cv2.resize(cropped_img, (32, 32))
        cv2.imwrite('./static/dataset/'+filename, final_img)


