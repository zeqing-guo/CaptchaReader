'''
Created on Aug 28, 2014

@author: Jason Guo E-mail: zqguo@zqguo.com
'''

import os
from PIL import Image

from Model import config

def split():
    directory = config.BINARY_CAPTCHA_DIR
    target_dir = config.LETTER_DIR
    print("Start to split figure...")
    for f in os.listdir(directory):
        if not f.endswith(".png"):
            continue

        img = Image.open(directory + f)
        img = img.convert("RGBA")
        black_pix = range(img.size[0])
        pixdata = img.load()

        for x in xrange(img.size[0]):
            row_black_pix = 0
            for y in xrange(img.size[1]):
                if pixdata[x, y] == (0, 0, 0, 255):
                    row_black_pix += 1
            black_pix[x] = row_black_pix
            
        split_position = []
        for i in xrange(1, img.size[0]):
            if black_pix[i] != 0 and black_pix[i - 1] == 0:
                if len(split_position) % 2 == 0:
                    split_position.append(i)
            elif black_pix[i] == 0 and black_pix[i - 1] != 0:
                if i - 1 - split_position[-1] >= 6:
                    split_position.append(i - 1)
        
        if split_position[1] > 17:
            insert_index(1, 10, 16, black_pix, split_position)
        if split_position[3] > 27:
            insert_index(3, 20, 26, black_pix, split_position)
        if split_position[5] > 37:
            insert_index(5, 30, 36, black_pix, split_position)
        if split_position[7] > 47:
            insert_index(7, 40, 46, black_pix, split_position)
        if len(split_position) != 8:
            return "alreadfail"

        region = img.crop((split_position[0], 0, split_position[1] + 1, img.size[1]))
        region.save("%s%s%02d.png" % (target_dir, f[0 : -4], 1))
        region = img.crop((split_position[2], 0, split_position[3] + 1, img.size[1]))
        region.save("%s%s%02d.png" % (target_dir, f[0 : -4], 2))
        region = img.crop((split_position[4], 0, split_position[5] + 1, img.size[1]))
        region.save("%s%s%02d.png" % (target_dir, f[0 : -4], 3))
        region = img.crop((split_position[6], 0, split_position[7] + 1, img.size[1]))
        region.save("%s%s%02d.png" % (target_dir, f[0 : -4], 4))

    print("Finish!")


def insert_index(index, low, high, black_pix, split_position):
    min_index = 0
    min_value = 25
    if split_position[index] > high:
        for i in range(low, high):
            if min_value > black_pix[i]:
                min_value = black_pix[i]
                min_index = i
        split_position.insert(index, min_index)
        split_position.insert(index + 1, min_index + 1)


split()