'''
Created on Aug 28, 2014

@author: Jason Guo E-mail: zqguo@zqguo.com
'''

import cStringIO
import datetime

from sklearn.externals import joblib

from PIL import Image

import config

class Identify():
    '''
    Usage: to identify the captcha.
    Input: the string of captcha image
    Output: the string of captcha content
    '''


    def __init__(self, captcha):
        '''
        Constructor
        '''
        self.captcha = captcha
        # Get the module
        self.clf = joblib.load(config.DATA_FILE_NAME)

    def captcha_reader(self):
        starttime = datetime.datetime.now()
        # Binarization
        captcha_file = cStringIO.StringIO(self.captcha)
        img = Image.open(captcha_file)
        img = img.convert("RGBA")
        black_pix = range(img.size[0])
        pixdata = img.load()
        
        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][0] < 90 or pixdata[x, y][1] < 162:
                    pixdata[x, y] = (0, 0, 0, 255)
                if pixdata[x, y][2] > 0:
                    pixdata[x, y] = (255, 255, 255, 255)
                else:
                    pixdata[x, y] = (0, 0, 0, 255)
                
        endtime = datetime.datetime.now()
        interval = endtime - starttime
        print "%.5f," % (interval.seconds + interval.microseconds / 1000000.0),        
        
       
        starttime = datetime.datetime.now()
        # Split figure
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
            self.insert_index(1, 10, 16, black_pix, split_position)
        if split_position[3] > 27:
            self.insert_index(3, 20, 26, black_pix, split_position)
        if split_position[5] > 37:
            self.insert_index(5, 30, 36, black_pix, split_position)
            
        if len(split_position) != 8:
            return "alreadfail"
        
        endtime = datetime.datetime.now()
        interval = endtime - starttime
        print "%.5f," % (interval.seconds + interval.microseconds / 1000000.0),        

 
        starttime = datetime.datetime.now()
        
        # Identify figure
        result = ""
        identify_list = black_pix[split_position[0] : split_position[1] + 1]
        identity_len = len(identify_list)
        while identity_len < 11:
            identify_list.append(0)
            identity_len += 1
        while identity_len > 11:
            identify_list.pop()
            identity_len -= 1
        result += self.clf.predict([identify_list])[0]
        
        identify_list = black_pix[split_position[2] : split_position[3] + 1]
        identity_len = len(identify_list)
        while identity_len < 11:
            identify_list.append(0)
            identity_len += 1
        while identity_len > 11:
            identify_list.pop()
            identity_len -= 1
        result += self.clf.predict([identify_list])[0]
       
        identify_list = black_pix[split_position[4] : split_position[5] + 1]
        identity_len = len(identify_list)
        while identity_len < 11:
            identify_list.append(0)
            identity_len += 1
        while identity_len > 11:
            identify_list.pop()
            identity_len -= 1
        result += self.clf.predict([identify_list])[0]
        
        identify_list = black_pix[split_position[6] : split_position[7] + 1]
        identity_len = len(identify_list)
        while identity_len < 11:
            identify_list.append(0)
            identity_len += 1
        while identity_len > 11:
            identify_list.pop()
            identity_len -= 1
        result += self.clf.predict([identify_list])[0]
        
        endtime = datetime.datetime.now()
        interval = endtime - starttime
        print "%.5f," % (interval.seconds + interval.microseconds / 1000000.0),   
        return result
    
    def insert_index(self, index, low, high, black_pix, split_position):
        min_index = 0
        min_value = 25
        if split_position[index] > high:
            for i in range(low, high):
                if min_value > black_pix[i]:
                    min_value = black_pix[i]
                    min_index = i
            split_position.insert(index, min_index)
            split_position.insert(index + 1, min_index + 1)  
        