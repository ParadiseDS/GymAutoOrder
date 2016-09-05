# -*- coding:utf8 -*-
# TODO:
# 1. 检测系统当前时间，若大于0点小于八点则在当天预约（有两处要修改，login delay=0，order delay=2）
# 2. 手机号输入
# 3. 伙伴id输入
"""
程序在当晚12点前启动,第二天早晨预约2天后的场地	
2015-12-23 18:38:05
xuchen
"""

import urllib2
import urllib
import cookielib
import gzip
from PIL import Image
from StringIO import StringIO
import zlib
import os
import datetime
import time
import thread

import PicProcess

DATEFORMAT_Ymd = '%Y-%m-%d'
DATEFORMAT_YmdHMS = '%Y-%m-%d %H:%M:%S'
todaydelta = (0 if datetime.datetime.now().hour < 8 else 1)

class OrderRobot:
	def __init__(self):
		self.headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'
		}
		self.loginUrl = 'http://myold.seu.edu.cn/userPasswordValidate.portal'
		self.validateimageUrl = 'http://yuyue.seu.edu.cn/eduplus/control/validateimage'
		self.postOrderUrl = 'http://yuyue.seu.edu.cn/eduplus/order/order/insertOredr.do?sclId=1'
		today = datetime.date.today()

		self.orderday = today + datetime.timedelta(days=2+todaydelta)
		self.cookie = cookielib.CookieJar()    
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
		self.username = raw_input('username>')
		self.password = raw_input('password>')
		self.time = {'15':' 15:00-16:00', '16':' 16:00-17:00', '17':' 17:00-18:00', '18':' 18:00-19:00', '19':' 19:00-20:00', '20':' 20:00-21:00'}
		self.t = raw_input('starttime: \n(17 represents 5:00pm - 6:00 pm)\n>')
		self.starttime = self.time[self.t]
		self.loginPostdata=urllib.urlencode({    
			'Login.Token1':self.username,
			'Login.Token2':self.password,
			'goto':'http://myold.seu.edu.cn/loginSuccess.portal',
			'gotoOnFail':'http://myold.seu.edu.cn/loginFailure.portal'    
		})  
		self.friendId = '75496'
		self.islogin = False
		
	def setFriend(self, name):
		self.friendId = self.friends[name]
	
	def login(self):
		req = urllib2.Request(    
			url = self.loginUrl,    
			data = self.loginPostdata,
			headers = self.headers
		)
		thread.start_new_thread(self.loginthread, (1,req))  
		thread.start_new_thread(self.loginthread, (2,req))  
		thread.start_new_thread(self.loginthread, (3,req))
	
	def loginthread(self, no, req):
		print('loginthread:%d\n' % no)
		result = self.opener.open(req) 
		for c in self.cookie:
			print 'cookie: '+c.name
			print 'value: '+c.value
		
		self.islogin = True
		
	def orderBadminton(self):
		validateResult = self.opener.open(self.validateimageUrl)
		validateNum = PicProcess.getResutlFromStr(validateResult.read()) 
		orderPostdata = urllib.urlencode({
			'orderVO.useTime':self.orderday.strftime(DATEFORMAT_Ymd)+self.starttime,
            'orderVO.itemId':'10',
			'orderVO.useMode':'2',
			'useUserIds':'77400',
			'orderVO.phone':'13736542156',
			'orderVO.remark':'',
			'validateCode':validateNum
		})
		req = urllib2.Request(    
			url = self.postOrderUrl,    
			data = orderPostdata,
			headers = self.headers
		)
		result = self.opener.open(req)
		return result.read()


now = datetime.datetime.now()

nextDay = now + datetime.timedelta(days=todaydelta)
#登陆时间 8:00:00s
loginTime = datetime.datetime(nextDay.year, nextDay.month, nextDay.day , 8, 0, 0)	
#登出时间 8:04:00s
exitTime = datetime.datetime(nextDay.year, nextDay.month, nextDay.day , 8, 4, 0)

myOrderRobot = OrderRobot()

while(now < loginTime):
	now = datetime.datetime.now()
	time.sleep(1)
	print "Login Time: %s Now: %s Target Time: %s" % (loginTime, now, myOrderRobot.orderday)

myOrderRobot.login()

isSuccess = False

while not myOrderRobot.islogin:
	continue
	
while(not(isSuccess) and now < exitTime):
	now = datetime.datetime.now()
	print isSuccess
	result = myOrderRobot.orderBadminton()
	if result == 'success':
		isSuccess = True
		print 'succcess'
	time.sleep(1)


