import asyncio
class Activator:
	def __init__(self, name, packet_stream=None):
		self.ps = None
		self.name = name
		self.future = None
		if packet_stream:
			self.set_packet_stream(packet_stream)
			
	@_core.module_cmd
	def wait_activator(self):
		print('waiting for activator')
		
	def on_recv(self, pkt):
		if self.future and pkt[0] == 0:
			self.future.set_result(1)

	def set_packet_stream(self, ps):
		ps.recv = self.on_recv
		self.ps = ps
