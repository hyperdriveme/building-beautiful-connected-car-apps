# MIT License
#
# Copyright (c) 2017 HyperdriveMe, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from json import dumps
import time

#note this lives in the root of the repo. it needs to be moved into this folder
import obd
import os

obdcmds = [
	obd.commands.RPM,
	obd.commands.SPEED,
	obd.commands.MAF
]

def scanobd():
	print 'scanobd started...'
	connection = obd.OBD()

	while True:
		frameData = {
			'TIME' : timestamp()
		}
		for cmd in obdcmds:
			try:
				response = connection.query(cmd)
				data = response.value
				print '>>', cmd.name, ':', data
			except: 
				data = None

			frameData[cmd.name] = data

		logdata('../_data/obd.log', dumps(frameData))
		time.sleep(1)


def logdata(filename, content):
	try:
		fout = open(filename, 'a')
		fout.write(content+'\n')
		fout.close()
	except Exception, inst:
		print 'logdata.write.error:', inst


def timestamp(timestamp=None):
	if timestamp is None:
		timestamp = time.time()
	return int(timestamp)

scanobd()