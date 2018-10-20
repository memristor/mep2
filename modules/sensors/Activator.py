from core.Util import asyn
from operator import add
import asyncio
class Activator:
	def __init__(self, name, packet_stream=None):
		self.ps = None
		self.name = name
		self.future = None
		if packet_stream:
			self.set_packet_stream(packet_stream)
			
	@asyn
	def wait_activator(self):
		print('waiting for activator')
		pass
		
	def on_recv(self, pkt):
		if self.future and pkt[0] == 0:
			self.future.set_result(1)

	def set_packet_stream(self, ps):
		ps.recv = self.on_recv
		self.ps = ps
