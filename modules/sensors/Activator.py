import asyncio
class Activator:
	def __init__(self, name, packet_stream=None):
		self.ps = None
		self.name = name
		self.future = None
		self.data = 0
		self.logic = 0
		self.state = 'chinch_ready'
		if packet_stream:
			self.set_packet_stream(packet_stream)
			
	@_core.module_cmd
	def wait_activator(self):
		pass
		
	@_core.module_cmd
	def check_activator(self):
		print('checking act')
		if self.data:
			self.future.set_result(1)
		else:
			self.state = 'check_chinch'
			print('checking for chinch')

	def export_cmds(self):
		_core.export_cmd('wait_activator', self.wait_activator)
		_core.export_cmd('check_activator', self.check_activator)
	
	def on_recv(self, pkt):
		if self.state == 'check_chinch' and self.future and pkt[0] == self.logic:
			self.future.set_result(1)
			self.state = 'chinch_ready'
			print('waiting for chinch')
			
		if self.state == 'chinch_ready' and self.future and pkt[0] == (self.logic^1):
			self.future.set_result(1)
			print('chinch GO GO GO')
	def set_packet_stream(self, ps):
		ps.recv = self.on_recv
		self.ps = ps
