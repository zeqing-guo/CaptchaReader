# -*- coding: UTF-8 -*-
'''
Created on Jul 13, 2014

Modified on Aug 28, 2014

@author: Jason Guo E-mail: zqguo@zqguo.com
'''
import urllib
import urllib2
import cookielib
import datetime

from sklearn.externals import joblib

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
            if count > 1:
                break
        print("total: %d, success: %d" % (count, success_num))
       
        