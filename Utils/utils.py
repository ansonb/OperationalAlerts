import json

def getRequestJson(request):
	reqStr = request.body.decode('utf-8')
	reqStrArr = reqStr.split()
	reqStr = ' '.join(reqStrArr)
	requestBody = json.loads(reqStr)

	return requestBody