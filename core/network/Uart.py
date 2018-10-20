#!/usr/bin/python3
import asyncio
import serial
from .Stream import Stream
from .packet.PacketStream import PacketStream
class Uart:
	def __init__(self, name='uart', baud=57600, dev='/dev/ttyAMA0'):
		self.name = name
		self.timeout = 0.01
		self.f = serial.Serial(dev, baud, timeout=self.timeout)
		self.flush()
		self.stream = Stream(self.send)
		
	def run(self):
		asyncio.ensure_future(self.read())
		
	async def read(self):
		while True:
			await asyncio.sleep(self.timeout)
			if self.f.in_waiting > 0:
				self.stream.recv(self.f.read(self.f.in_waiting))
				
	def send(self, x):
		self.f.write(x)
		
	def flush(self):
		self.f.flushInput()
		
	def get_stream(self):
		return self.stream
		
	def get_packet_stream(self):
		from .packet.UartPacket import UartPacket
		return UartPacket(self.get_stream())
