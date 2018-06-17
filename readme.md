Requirements
===================
1) Python 3
2) mongodb

Installation
===================
pip install -r requirements.txt

Starting the server locally
===========================
python manage.py runserver 0.0.0.0:8000

Testing
===================
1) /bills/pay
--------------
url: http://18.219.46.23:8000/bills/pay

method: POST

request body: 
{
	"userid": 1787651,
	"ts": "20180605 184300",
	"latlong": "19.07, 72.87",
	"timespent": 72,
	"properties": {
		"bank": "hdfc",
		"merchantid": 234,
		"value": 130009.5,
		"mode": "netbank"
	}
}

response:
{
    "success": true,
    "message": "Bill payment completed successfully"
}

2) /fdbk/post
-------------
url: http://18.219.46.23:8000/fdbk/post

method: POST

request body:
{
	"userid": 1787651,
	"ts": "20180605 184302",
	"latlong": "19.07, 72.87",
	"timespent": 72,
	"properties": {
		"text": "some feedback"
	}
}

response:
{
    "success": true,
    "message": "Feedback posted successfully"
}

3) Checking log file
---------------------
http://18.219.46.23:8000/static/logs.txt

TODO
=======================
1) Testing parameter types and char len before storing in database
2) Error handling
