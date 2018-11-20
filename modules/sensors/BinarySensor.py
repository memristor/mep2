class BinarySensor:
	def __init__(self, name, state=False, packet_stream=None):
		self.ps = None
		self.name = name
		self.future = None
		self.state = state
		if packet_stream:
			self.set_packet_stream(packet_stream)
			
	@_core.module_cmd
	def wait_state(self, state):
		self.trigg_on_state = state
	
	def set(self, state):
		self.ps.send(bytes[self.state])
		
	def get(self):
		return self.state
	
	def on_recv(self, pkt):
		if self.future and pkt[0] == self.trigg_on_state:
			self.future.set_result(1)
		self.state = pkt[0]

	def export_cmds(self):
		_core.export_cmd('wait_state', wait_state)
		
	def set_packet_stream(self, ps):
		ps.recv = self.on_recv
		self.ps = ps
