'''
Created on Aug 28, 2014

@author: Jason Guo E-mail: zqguo@zqguo.com
'''

import os
from PIL import Image

from Model import config

def Thresholding():
    print("Start to binarize...")
    for f in os.listdir(config.CAPTCHA_DIR):
        if f.endswith(".png"):
            img = Image.open(config.CAPTCHA_DIR + f)
            img = img.convert("RGBA")
            pixdata = img.load()

            for y in xrange(img.size[1]):
                for x in xrange(img.size[0]):
                    if pixdata[x, y][0] < 90:
                        pixdata[x, y] = (0, 0, 0, 255)
                    if pixdata[x, y][1] < 162:
                        pixdata[x, y] = (0, 0, 0, 255)
                    if pixdata[x, y][2] > 0:
                        pixdata[x, y] = (255, 255, 255, 255)
                    else:
                        pixdata[x, y] = (0, 0, 0, 255)

            img.save(config.BINARY_CAPTCHA_DIR + f, "PNG")
    print("Finish!")

Thresholding()
