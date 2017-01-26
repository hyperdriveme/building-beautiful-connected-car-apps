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


import inspect, operator, os, time, types, sys, re, hashlib

from json import loads, dumps
from urlparse import parse_qs
from urllib import urlencode

from gevent.pywsgi import WSGIServer
import gevent


def parseAndDelistArguments(args): 
	if type(args) in [types.StringType, types.UnicodeType] and args[:1] in ['{', '[']:
		args = loads(args)
		if type(args) in [types.ListType, types.ListType]: return args;
	else:
		args = parse_qs(args)
	return delistArguments(args);


def delistArguments(args):
	'''
		Takes a dictionary, 'args' and de-lists any single-item lists then
		returns the resulting dictionary.
		{'foo': ['bar']} would become {'foo': 'bar'}
	'''
	
	def flatten(k,v):
		if len(v) == 1 and type(v) is types.ListType: return (str(k), v[0]);
		return (str(k), v)

	return dict([flatten(k,v) for k,v in args.items()])

def application(env, start_response):

	verb = env['REQUEST_METHOD']
	path = env['PATH_INFO']
	
	args = parseAndDelistArguments(env['QUERY_STRING'])
	if 'verb' in args: 
		verb = args['verb'].upper()
		del args['verb']

	print 'args: ', args
	print 'path: ', path

	if path == '/favicon.ico': 
 		start_response('301 Moved Permanently', [('Location', 'http://hyperdrive.me/favicon.ico')])
 		return ''

# 	domain = args['domain']
# 	path = args['path'][1:]
# 	persisted_data = domains.get(domain)

	start_response('200 OK', [('Content-Type', 'text/plain')])
	return 'true'

if __name__ == '__main__':
	wsgi_port = 8882
	print 'serving on %s...' % wsgi_port
	WSGIServer(('', wsgi_port), application).serve_forever()


# http://localhost:8882/hello?data=world