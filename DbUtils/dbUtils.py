import sys
sys.path.append('utils')
import config

from pymongo import MongoClient
import time

class DbUtils():

	def __init__(self):
		self.db = self.connect()
		self.userCollection = self.db.userCollection
		self.adminCollection = self.db.adminCollection
		

	def connect(self):
		client = MongoClient()
		client = MongoClient(config.ConnectorConfig.mongoIp,config.ConnectorConfig.port)
		db = client.OperationalAlerts
		return  db

	def insertIntoCustomerDb(self, schema):
		_id = self.userCollection.insert(schema)
		return _id

	def insertIntoAdminDb(self, schema):
		_id = self.adminCollection.insert(schema)
		return _id		

	def findUserBills(self, userid, startTime=0, endTime=time.time()):
		userBills = self.userCollection.find( {'$and':[ {'userid': userid }, { 'timestamp_in_seconds': { '$gte': startTime } }, { 'timestamp_in_seconds': { '$lte': endTime } }, { 'noun': 'bill' } ] } )
		
		userBills = list(userBills)

		print('userBills')
		print(userBills)
		return userBills

	def getUserFeedbacks(self, userid, startTime=0, endTime=time.time()):
		print('startTime')
		print(startTime)
		print('endTime')
		print(endTime)
		userFeedbacks = self.userCollection.find( {'$and':[ {'userid': userid }, { 'timestamp_in_seconds': { '$gte': startTime } }, { 'timestamp_in_seconds': { '$lte': endTime } }, { 'noun': 'fdbk' } ] } )
		
		userFeedbacks = list(userFeedbacks)

		print('userFeedbacks')
		print(userFeedbacks)
		return userFeedbacks		