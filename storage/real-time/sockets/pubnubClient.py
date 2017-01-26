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

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException

pnconfig = PNConfiguration()
pnconfig.publish_key   = '< pubnub publish key >'
pnconfig.subscribe_key = '< pubnub subscribe key >'
pnconfig.ssl = False
pnchannel ='< pubnub channel >'

pn = PubNub(pnconfig)

class MyListener(SubscribeCallback):
    def status(self, pubnub, status):
		# pn.publish().channel("Channel-1i00ruwan").message({'fieldA': 'awesome', 'fieldB': 10}).sync()
        print 'status:', pubnub, status
 
    def message(self, pubnub, message):
        print 'message:', pubnub, message.message
        pass
 
    def presence(self, pubnub, presence):
        print 'presence:', pubnub, presence
        pass
 
my_listener = MyListener()
pn.add_listener(my_listener)
pn.subscribe().channels(pnchannel).execute()

def send():
	try:
		envelope = pn.publish().channel(pnchannel).message({
			"name" : "message",                  ## Event Name
			"ns"   : "standard-%s" % pnchannel, ## Namespace
			"data" : { "my" : "data" }           ## Your Message
		}).sync()
		print("publish timetoken: %d" % envelope.result.timetoken)
	except PubNubException as e:
		print e
