#!/usr/bin/env python

import os
import json
import datetime
import psutil
import flask

app = flask.Flask(__name__)

class HWSerial(object):
	def __init__(self, name):
		self.name = name

class HWSerialEncoder(json.JSONEncoder):
	def default(self, o):
		return o.__dict__

@app.route('/api/v1/time')
def api_time():
	def utcconverter(o):
		if isinstance(o, datetime.datetime):
			return o.__str__()
	return json.dumps({'utc': datetime.datetime.utcnow()}, indent=4, default=utcconverter)

@app.route('/api/v1/status')
def api_status():
	return json.dumps({'cpu': psutil.cpu_percent()}, indent=4)

@app.route('/api/v1/serializer', methods=['POST'])
def api_serializer():
	name = flask.request.values.get('name')
	serial = HWSerial(name)
	return json.dumps(serial, indent=4, cls=HWSerialEncoder)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=os.environ.get('HWSERIAL_PORT', 5000))
