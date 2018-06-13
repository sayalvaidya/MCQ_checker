# coding: utf-8
from scipy.misc import imread
import numpy as np
import pandas as pd
import os
import cv2



root = 'C:/Users/Anushka/PycharmProjects/test/finalDataSet/30'  # or ‘./test’ depending on for which the CSV is being created

# go through each directory in the root folder given above
for directory, subdirectories, files in os.walk(root):
    # go through each file in that directory
    for file in files:
        # read the image file and extract its pixels
        im = imread(os.path.join(directory, file))
        value = im.flatten()
        # I renamed the folders containing digits to the contained digit itself. For example, digit_0 folder was
        # renamed to 0. so taking the 9th value of the folder gave the digit (i.e. "./train/8" ==> 9th value is 8),
        # which was inserted into the first column of the data_set.
        value = np.hstack((directory[54:], value))
        df = pd.DataFrame(value).T
        df = df.sample(frac=1)  # shuffle the data_set
        with open('test.csv', 'a') as data_set:
            df.to_csv(data_set, header=False, index=False)

#
# img = imread("test1.png")
# dimg = cv2.resize(img, (32,32), interpolation=cv2.INTER_AREA)
# cv2.imwrite("resizedImage.png", dimg)


# root = 'C:\\Users\\Babu Sabin\\Desktop\\sample'  # or ‘./test’ depending on for which the CSV is being created
# root_output = 'C:\\Users\\Babu Sabin\\Desktop\\mul'
# i = 1000
# # go through each directory in the root folder given above
# for directory, subdirectories, files in os.walk(root):
#     # go through each file in that directory
#     for file in files:
#         # read the image file and extract its pixels
#         img = imread(os.path.join(directory, file))
#         imr = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
#         dimg = cv2.cvtColor(imr, cv2.COLOR_BGR2GRAY)
#         row, col = dimg.shape[:2]
#         bottom = dimg[row - 2:row, 0:col]
#         bordersize = 2
#         borderImage = cv2.copyMakeBorder(dimg, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize,
#                                     borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])
#         cv2.imwrite(root_output+'\\'+str(i)+".jpg", borderImage)
#         i += 1