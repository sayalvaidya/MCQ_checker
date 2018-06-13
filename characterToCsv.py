from scipy.misc import imread
import numpy as np
import pandas as pd
import os
import cv2
from os.path import join, dirname, realpath


UPLOAD_FOLDER_CHARACTER_CSV = join(dirname(realpath(__file__)), 'static/characterCsv/')
FOLDER_DIGITS_SEGMENTED_IMAGES = join(dirname(realpath(__file__)), 'static/digitSegmentedImages/')


def character_to_csv(character_img_file):
    img = imread(FOLDER_DIGITS_SEGMENTED_IMAGES+character_img_file,0)
    im = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
    # im = cv2.cvtColor(imgr, cv2.COLOR_BGR2GRAY)
    row, col = im.shape[:2]
    bottom = im[row - 2:row, 0:col]
    bordersize = 2
    border = cv2.copyMakeBorder(im, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize,
                                borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])
    value = border.flatten()
    new_name = character_img_file.split('.')
    df = pd.DataFrame(value).T
    df = df.sample(frac=1)  # shuffle the dataset
    with open(str(UPLOAD_FOLDER_CHARACTER_CSV)+new_name[0]+'.csv', 'a') as dataset:
        df.to_csv(dataset, header=False, index=False)
    return new_name[0]+'.csv'
