
########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2014 Brendan Whitfield (bcw7044@rit.edu)                   #
#                                                                      #
########################################################################
#                                                                      #
# port.py                                                              #
#                                                                      #
# This file is part of python-OBD (a derivative of pyOBD)              #
#                                                                      #
# python-OBD is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 2 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# python-OBD is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with python-OBD.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                      #
########################################################################

import serial
import string
import time
from utils import Response, unhex
from debug import debug

import socket

class State():
	""" Enum for connection states """
	Unconnected, Connected = range(2)

class OBDPort:
	""" OBDPort abstracts all communication with OBD-II device."""

	def __init__(self, portname):
		"""Initializes port by resetting device and gettings supported PIDs. """

		ipaddr = "192.168.0.10"
		ipport = 35000

		# These should really be set by the user.
		baud     = 38400
		databits = 8
		parity   = serial.PARITY_NONE
		stopbits = 1
		timeout  = 2 #seconds

		self.ELMver = "Unknown"
		self.state  = State.Unconnected
		self.port   = None

		debug("Opening wifi connection...")

		try:
			self.port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.port.connect((ipaddr, ipport))

		except Exception, inst: 
			self.error(inst)
			return

		debug("Wifi successfully connected @ %s:%s" % (ipaddr, ipport))

		try:
			self.send("atz")   # initialize
			time.sleep(1)
			self.ELMver = self.get()

			if self.ELMver is None :
				self.error("ELMver did not return")
				return
			
			debug("atz response: " + self.ELMver)
		
		except Exception, inst: 
			self.error(inst)
			return

		self.send("ate0")  # echo off
		debug("ate0 response: " + self.get())
		debug("Connected to ECU")
		self.state  = State.Connected

	def error(self, msg=None):
		""" called when connection error has been encountered """
		debug("Connection Error:", True)

		if msg is not None: debug(msg, True);
		if self.port is not None: self.port.close();
		
		self.state = State.Unconnected

	def get_port_name(self):
		return str(self.port) if (self.port is not None) else "No Port"

	def is_connected(self):
		return self.state == State.Connected

	def close(self):
		""" Resets device and closes all associated filehandles"""

		if self.port is not None and self.state == State.Connected:
			self.send("atz")
			self.port.close()

		self.port = None
		self.ELMver = "Unknown"

	# sends the hex string to the port
	def send(self, cmd):
		if self.port:
			if self.port.send(cmd+"\r") <= 0: 
				print("Failed to send the data")
				return

	# accumulates and returns the ports response
	def get(self):
		"""Internal use only: not a public interface"""

		attempts = 2
		result = ""

		if self.port is not None:
			while 1:
				c = self.port.recv(1)

				# if nothing was recieved
				if len(c) == 0:

					if(attempts <= 0):
						break

					debug("get() found nothing")
					
					attempts -= 1
					continue

				# skip carraige returns
				if c == '\r':
					continue

				# end on chevron
				if c == ">":
					break;
				else: # whatever is left must be part of the response
					result = result + c
		else:
			debug("NO self.port!", True)

		return result