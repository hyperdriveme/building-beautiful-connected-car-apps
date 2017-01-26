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

import cStringIO
import gzip
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from json import loads, dumps

#set these
AccessKey = '<aws access key>' 
SecretKey = '<aws secret key>'
BucketName = '<hyperdrive-beautiful-<unique name>'

conn = S3Connection(AccessKey, SecretKey)
b = conn.create_bucket(BucketName)

def compress_string(s):
	zbuf = cStringIO.StringIO()
	zfile = gzip.GzipFile(mode='wb', compresslevel=9, fileobj=zbuf)
	zfile.write(s)
	zfile.close()
	return zbuf.getvalue()


def decompress_string(s):
	zbuf = cStringIO.StringIO(s)
	f = gzip.GzipFile(mode='rb', fileobj=zbuf)
	try:
		ret = f.read()
	finally:
		f.close()
	return ret


def load_file(filename):
	try:
		if os.path.exists(filename): 
			return file(filename).readlines()

	except Exception, inst:
		print 'file_get.error:', filename, inst


def put_file(filename, data):
	k = Key(b)
	k.key = filename

	data = compress_string(data)
	headers = {'Content-Encoding' : 'gzip'}

	try:
		k.set_contents_from_string(data, headers, replace=True)

	except Exception, inst:
		if repr(inst).strip() == 'S3ResponseError: 100 Continue': 
			k.make_public();
			print 'addFile -> done putting file'


def get_file(filename):
	k = Key(b)
	k.key = filename
	
	data = k.get_contents_as_string()
	try:
		return decompress_string(data)
	except:
		return data


# get the log file
sendData = '\r'.join(load_file('../../_data/obd.log'))
# send to s3
put_file('obd.log', dumps(sendData))

# get from s3
returnData = get_file('obd.log')
returnData = loads(returnData)

# check to see if the data matches
print 'data matches:', sendData == returnData