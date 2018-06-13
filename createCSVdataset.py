from scipy.misc import imread
import numpy as np
import pandas as pd
import os
import cv2


root = '\\Users\\sayalvaidya\\PycharmProjects\\by_class'  # or ‘./test’ depending on for which the CSV is being created

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
        value = np.hstack((directory[51:], value))
        df = pd.DataFrame(value).T
        df = df.sample(frac=1)  # shuffle the data_set
        with open('test.csv', 'a') as data_set:
            df.to_csv(data_set, header=False, index=False)
