from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse

import sys
sys.path.append('DbUtils')
sys.path.append('Utils')
sys.path.append('AdminOps')
from dbUtils import DbUtils
import utils
import config
from adminOps import AdminOps

import time
import datetime
from threading import Thread
from time import sleep

# Create your views here.
class Api():

	def __init__(self):
		self.dbInstance = DbUtils()
		self.adminOps = AdminOps()
		
	def isFirstBillPayment(self, userid):
		userBills = self.dbInstance.findUserBills(userid)
		return len(userBills)==0

	def excessBillsPaid(self, userid, paymentTime):
		userBills = self.dbInstance.findUserBills(userid, startTime=paymentTime-config.TIME_INTERVAL_FOR_BILL_PAYMENT, endTime=paymentTime)
		amount = 0
		for bill in userBills:
			amount += bill['properties']['value']

		print('amount')
		print(amount)
		print('len(userBills)')
		print(len(userBills))

		return len(userBills)>=config.LIMIT_ON_NUMBER_OF_BILLS and amount>=config.LIMIT_ON_AMOUNT_OF_BILLS, amount


	def checkFeedbackReceived(self, userid, startTime, endTime):
		userFeedbacks = self.dbInstance.getUserFeedbacks(userid, startTime=startTime, endTime=endTime)
		return len(userFeedbacks)>0

	def setTimer(self, userid, secondsToWait, startTime):
		print('going to sleep for {} s'.format(secondsToWait))
		sleep(secondsToWait)
		print('Done sleeping')
		endTime = startTime + secondsToWait
		feedbackReceived = self.checkFeedbackReceived(userid,startTime,endTime)
		print('feedbackReceived')
		print(feedbackReceived)
		if not feedbackReceived:
			self.adminOps.alertCubeUser(userid)


	@csrf_exempt
	def payBill(self, request):
		requestBody = utils.getRequestJson(request)

		timestamp = time.mktime(datetime.datetime.strptime(requestBody['ts'], '%Y%m%d %H%M%S').timetuple())

		schema = {
			'noun': 'bill', #TODO: add constants
			'userid': requestBody['userid'],
			'ts': requestBody['ts'], #TODO: timestamp should be from server?
			'latlong': requestBody['latlong'],
			'verb': 'pay',
			'timespent': requestBody['timespent'],
			'properties': requestBody['properties'],
			'timestamp_in_seconds': timestamp
		}

		if self.isFirstBillPayment(requestBody['userid']):
			self.adminOps.sendPushNotification(requestBody['userid'])

		self.dbInstance.insertIntoCustomerDb(schema)

		# obj = self
		_thread = Thread(target=self.setTimer, args=(requestBody['userid'],config.SECONDS_TO_WAIT_FOR_ADMIN_ALERT,timestamp))
		_thread.start()

		isExcessBillsPaid, amount = self.excessBillsPaid(requestBody['userid'],timestamp)
		if isExcessBillsPaid:
			self.adminOps.alertUser(requestBody['userid'],amount)

		return JsonResponse({
				'success': True,
				'message': 'Bill payment completed successfully'
			})

	@csrf_exempt
	def postFeedback(self, request):
		requestBody = utils.getRequestJson(request)

		schema = {
			'noun': 'fdbk', #TODO: add constants
			'userid': requestBody['userid'],
			'ts': requestBody['ts'], #TODO: timestamp should be from server?
			'latlong': requestBody['latlong'],
			'verb': 'post',
			'timespent': requestBody['timespent'],
			'properties': requestBody['properties'],
			'timestamp_in_seconds': time.mktime(datetime.datetime.strptime(requestBody['ts'], '%Y%m%d %H%M%S').timetuple())
		}

		self.dbInstance.insertIntoCustomerDb(schema)

		return JsonResponse({
				'success': True,
				'message': 'Feedback posted successfully'
			})
