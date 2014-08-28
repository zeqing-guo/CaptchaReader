'''
Created on Aug 28, 2014

@author: Jason Guo E-mail: zqguo@zqguo.com
'''
import os
from sklearn.externals import joblib
from PIL import Image

from Model import config

def classify():
    clf = joblib.load(config.DATA_FILE_NAME)
    directory = config.LETTER_DIR
    target = config.CLASSIFIED_LETTER
    if not os.path.isdir(target):
        os.mkdir(target)
    print("Start to classify")

    for f in os.listdir(directory):
        if not f.endswith(".png"):
            continue

        img = Image.open(directory + f)
        img = img.convert("RGBA")
        pixdata = img.load()

        identity_value = []

        for x in xrange(img.size[0]):
            row_count = 0
            weight = 1
            for y in xrange(img.size[1]):
                if pixdata[x, y] == (0, 0, 0, 255):
                    row_count += weight
            identity_value.append(row_count)
            
        identity_len = len(identity_value)
        while identity_len < 11:
            identity_value.append(0)
            identity_len += 1
        while identity_len > 11:
            identity_value.pop()
            identity_len -= 1
        newname = clf.predict([identity_value])[0] + "zxc" + f

        os.rename(directory + f, target + newname)

    print("Finish!")
    
classify()