# -*- coding: UTF-8 -*-
'''
Created on Jul 13, 2014

@author: Jason Guo E-mail: zqguo@zqguo.com
'''
import datetime
import Tkinter as tk

from Control.CourseSelection import CourseSelection

class Main():
    '''
    This is the main View of the program
    '''
    
    def __init__(self):
        self.info = "当前状态："
        
        self.root = tk.Tk()
        
        self.function_frame = tk.Frame(self.root)
        self.info_frame = tk.Frame(self.root)
        
        self.function_frame.pack(side = tk.LEFT)
        self.info_frame.pack(side = tk.RIGHT)
        
        self.buttom_frame = tk.Frame(self.function_frame)
        self.input_frame = tk.Frame(self.function_frame)
        
        self.input_frame.pack(side = tk.TOP)
        self.buttom_frame.pack(side = tk.BOTTOM)
        
        self.right_frame = tk.Frame(self.input_frame)
        self.left_frame = tk.Frame(self.input_frame)
        
        # Show current status
        self.info_text = tk.StringVar()
        self.IM = tk.Message(self.info_frame, textvariable = self.info_text, width=500)
        self.info_text.set(self.info)
        self.IM.pack(side = tk.TOP)
        
        
        # Verification button
        self.BT = tk.Button(self.buttom_frame, text = "开始刷课", command = self.process_input)
        self.BT.pack(side = tk.LEFT)
        
        # Username label & username entry
        self.UL = tk.Label(self.left_frame, text = "用户名：")
        self.UE = tk.Entry(self.right_frame, bd = 2)
        
        # Password label & password entry
        self.PL = tk.Label(self.left_frame, text = "密码：")
        self.PE = tk.Entry(self.right_frame, bd = 2, show = "*")
        
        # Lesson's number label & lesson's number entry
        self.LL = tk.Label(self.left_frame, text = "选课号：")
        self.LE = tk.Entry(self.right_frame, bd = 2)
        
        self.UL.pack(side = tk.TOP)
        self.PL.pack(side = tk.TOP)
        self.LL.pack(side = tk.TOP)
        
        self.UE.pack(side = tk.TOP)
        self.PE.pack(side = tk.TOP)
        self.LE.pack(side = tk.TOP)
        
        self.left_frame.pack(side = tk.LEFT)
        self.right_frame.pack(side = tk.RIGHT)
        
        self.root.mainloop()
        
    def process_input(self):
        self.username = self.UE.get()
        self.password = self.PE.get()
        self.lesson_num = self.LE.get()
        
        starttime = datetime.datetime.now()
        cs = CourseSelection(self.username, self.password, self.lesson_num)
        cs.login()
        endtime = datetime.datetime.now()
        interval = endtime - starttime
        self.info = self.info + "\n登录共用时：%.2f秒" % (interval.seconds + interval.microseconds / 1000000.0)
        self.info_text.set(self.info)
    
    def update(self, text):
        self.info = self.info + text
        self.info_text.set(self.info)
        
    
        
        
        
        
        
        
        