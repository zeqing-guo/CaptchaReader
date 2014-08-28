# -*- coding: UTF-8 -*-
'''
Created on Jul 13, 2014

Modified on Aug 28, 2014

@author: Jason Guo E-mail: zqguo@zqguo.com
'''
import urllib
import urllib2
import cookielib
import cStringIO
import datetime

from sklearn.externals import joblib

from PIL import Image

import config
from Identify import Identify

class CourseSelection():
    '''
    The class is created for select course.
    '''
    def __init__(self, username, password, lesson_num):
        self.username = username
        self.password = password
        self.lesson_num = lesson_num
        self.is_login = False
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"}
        self.captcha = ""
        self.cj = cookielib.CookieJar()   
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        
        urllib2.install_opener(self.opener)     
        
        # Get the module
        self.clf = joblib.load(config.DATA_FILE_NAME)
        
    def login(self):
        count = 0
        success_num = 0
        print("编号,下载验证码,二值化,分割,识别,发送登录请求,状态")
        while not self.is_login:
            print "%3d," % (count + 1),
            # Get the login CAPTCHA
            req = urllib2.Request(config.LOGINCAPTCHAURL, headers = self.headers)
            starttime = datetime.datetime.now()
            image_response = self.opener.open(req)
            self.captcha = image_response.read()
            endtime = datetime.datetime.now()
            interval = endtime - starttime
            print "%.5f," % (interval.seconds + interval.microseconds / 1000000.0),
            identify = Identify(self.captcha)
            captcha_content = identify.captcha_reader()
            #captcha_content = self.captcha_reader()
            if len(captcha_content) != 4:
                file(config.FAIL_IMAGE + "%02d.png" % count, "wb").write(self.captcha);
                count += 1
                print("fail")
                continue
            
            # Start to login
            data = {
                    "studentId": self.username,
                    "password": self.password,
                    "rand": captcha_content,
                    "Submit2": "提交"
                    }
            req = urllib2.Request(config.LOGINURL, urllib.urlencode(data), headers = self.headers)
            starttime = datetime.datetime.now()
            login_response = self.opener.open(req)
            endtime = datetime.datetime.now()
            interval = endtime - starttime
            print "%.5f," % (interval.seconds + interval.microseconds / 1000000.0),
            if login_response.geturl() == "http://xk.fudan.edu.cn/xk/home.html":
                success_num += 1
                count += 1
                print("success")
            else:
                self.cj = cookielib.CookieJar()
                self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
                urllib2.install_opener(self.opener)
                file(config.FAIL_IMAGE + "%02d.png" % count, "wb").write(self.captcha);
                count += 1
                print("fail")
            if count > 500:
                break
        print("total: %d, success: %d" % (count, success_num))
                
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
        