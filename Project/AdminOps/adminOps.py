import time
import datetime

import sys
sys.path.append('Utils')
import config

import os

class AdminOps():

	def __init__(self):
		self.log_path = config.LOG_EVENTS_PATH
		# if not os.path.exists(self.log_path):
		# 	with open(self.log_path, 'w') as f:

	def log(self, msg):
		with open(self.log_path, 'a') as f:
			f.write(msg + '\n')

	def getFormattedCurTime(self):
		t = time.time()
		d = datetime.datetime.fromtimestamp(t)
		cur_time = d.strftime('%Y-%m-%d %H:%M:%S')
		return cur_time

	def sendPushNotification(self, userid):
		cur_time = self.getFormattedCurTime()
		msg = 'Sending push notification to user: {} at {}'.format(userid,cur_time)
		self.log(msg)

	def alertUser(self, userid, amount):
		print('alerting user')
		cur_time = self.getFormattedCurTime()
		msg = 'Alerting user {} about excess bill payment amounting to {} at {}'.format(userid,amount,cur_time)
		self.log(msg) 	

	def alertCubeUser(self, userid):
		cur_time = self.getFormattedCurTime()
		msg = 'Alerting Cube user about non receipt of feedback from user {}'.format(userid)
		self.log(msg) 	