'''
Created on Aug 28, 2014

@author: Jason Guo E-mail: zqguo@zqguo.com
'''

import urllib2

from Model import config

def download():
    print("Start to download figure...")
    for i in range(config.DOWNLOAD_NUMBER):
        fig = urllib2.urlopen(config.CAPTCHA_URL)
        file(config.CAPTCHA_DIR + "%02d.png" % i, "wb").write(fig.read())
    print("Finish!")

download()

