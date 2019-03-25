from core.Convert import *
class PressureSensor:
	def __init__(self, name, id, packet_stream=None):
		self.ps = None
		self.id = id
		self.name = name
		self.future = None
		if packet_stream:
			self.set_packet_stream(packet_stream)
	
	
	def on_recv(self, pkt):
		if len(pkt) >= 4:
			self.value = lu16l(pkt,0)
			self.future.set_result( self.value < 0x0400 )
			#self.future.set_result( self.value  )

	def export_cmds(self, ns=''):
		with _core.export_ns(ns):
			_core.export_cmd('picked', self.picked)
		
	@_core.module_cmd
	def picked(self):
		self.ps.send(bytes([self.id]))

	def set_packet_stream(self, ps):
		ps.recv = self.on_recv
		self.ps = ps
