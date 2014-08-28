'''
Created on Aug 28, 2014

@author: Jason Guo E-mail: zqguo@zqguo.com
'''

import os
import numpy as np
from sklearn.svm import SVC
from sklearn.externals import joblib
from PIL import Image

from Model import config

def generate():
    trainset = []
    label = []
    directory = config.TRAIN_SET_DIR
    DATA_FILE_NAME = config.DATA_FILE_NAME
    print("Start to generate model")

    for f in os.listdir(directory):
        if not f.endswith(".png"):
            continue

        img = Image.open(directory + f)
        img = img.convert("RGBA")
        pixdata = img.load()

        identify_value = []

        for x in xrange(img.size[0]):
            row_count = 0
            for y in xrange(img.size[1]):
                if pixdata[x, y] == (0, 0, 0, 255):
                    row_count += 1
            identify_value.append(row_count)

        label.append(f[0 : 1])
        identity_len = len(identify_value)
        while identity_len < 11:
            identify_value.append(0)
            identity_len += 1
        while identity_len > 11:
            identify_value.pop()
            identity_len -= 1
        trainset.append(identify_value)

    X = np.array(trainset)
    y = np.array(label)

    clf = SVC()
    clf.fit(X, y)
    joblib.dump(clf, DATA_FILE_NAME)

    print("Finish!")
    
generate()