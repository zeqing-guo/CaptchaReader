'''
Created on Jul 13, 2014

@author: Jason Guo E-mail: zqguo@zqguo.com
'''

import os
import urllib2
import json

from PIL import Image

import config

def download():
    if not os.path.isdir(config.CAPTCHA_DIR):
        os.mkdir(config.CAPTCHA_DIR)
    if not os.path.isdir(config.CAPTCHA_LETTER):
        os.mkdir(config.CAPTCHA_LETTER)
    if not os.path.isdir(config.CAPTCHA_MODULE):
        os.mkdir(config.CAPTCHA_MODULE)
        
    
    url = "http://xk.fudan.edu.cn/xk/image.do"
    print("Start to download figure...")
    for i in range(config.DOWNLOAD_NUMBER):
        fig = urllib2.urlopen(url)
        file("%s%02d.png" % (config.CAPTCHA_DIR, i), "wb").write(fig.read())
    print("Finish!")
    
def Thresholding():
    print("Start to do thresholding...")
    for f in os.listdir(config.CAPTCHA_DIR):
        if f.endswith(".png"):
            img = Image.open(config.CAPTCHA_DIR + f)
            img = img.convert("RGBA")
            pixdata = img.load()

            for y in xrange(img.size[1]):
                for x in xrange(img.size[0]):
                    if pixdata[x, y][0] < 90:
                        pixdata[x, y] = (0, 0, 0, 255)
                    if pixdata[x, y][1] < 136:
                        pixdata[x, y] = (0, 0, 0, 255)
                    if pixdata[x, y][2] > 0:
                        pixdata[x, y] = (255, 255, 255, 255)

            img.save(config.CAPTCHA_DIR + f, "PNG")
    print("Finish!")
    
def split():
    directory = config.CAPTCHA_DIR
    target_dir = config.CAPTCHA_LETTER
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

def import_module():
    module_dic = {}
    print("Start to import module")
    for f in os.listdir(config.CAPTCHA_MODULE):
        if not f.endswith(".png"):
            continue

        img = Image.open(config.CAPTCHA_MODULE + f)
        img = img.convert("RGBA")
        pixdata = img.load()

        identify_value = []

        for x in xrange(img.size[0]):
            row_count = 0
            for y in xrange(img.size[1]):
                if pixdata[x, y] == (0, 0, 0, 255):
                    row_count += 1
            identify_value.append(row_count)
        col_list = []
        for y in xrange(img.size[1]):
            col_count = 0
            for x in xrange(img.size[0]):
                if pixdata[x, y] == (0, 0, 0, 255):
                    col_count += 1
            col_list.append(col_count)
        col_list = filter(lambda x : x != 0,col_list)

        identify_value = identify_value + col_list
        identify_value = filter(lambda x : x != 0, identify_value)
        identify_str = "".join(str("%x" % e) for e in identify_value)
        if module_dic.has_key(f[0 : 1]):
            module_dic[f[0 : 1]].append(identify_str)
        else:
            module_dic[f[0 : 1]] = [identify_str]
#    for key in module_dic:
#        print("%s: %s" % (key, module_dic[key][0]))
    for key in module_dic:
        for i in module_dic[key]:
            print("%s: %s" % (key, i))
        print("")
    
    json_module = json.JSONEncoder().encode(module_dic)
    f_handle = open(config.DATA_FILE_NAME, "w")
    try:
        f_handle.write(json_module)
    finally:
        f_handle.close()
        
    print("Finish!")
    

#download()
#Thresholding()
#split()
import_module()
