from core.Util import *
import asyncio
class BinaryInfrared:
	def __init__(self, name, sensor_position, sensor_vector, sensor_map=None, packet_stream=None):
		self.ps=packet_stream
		if self.ps:
			self.set_packet_stream(self.ps)
		self.name = name
		self.enabled = True
		self.sensor_map = sensor_map
		self.sensor_position = sensor_position
		self.detected = False
		self.sensor_vector = sensor_vector
	
	async def loop(self):
		while 1:
			await asyncio.sleep(0.1)
			if self.detected:
				pt = add_pt(self.sensor_position, self.sensor_vector)
				self.sensor_map.add_sensor_point('infrared', self.name, self.sensor_position, pt)
				
	def on_recv(self, pkt):
		if self.enabled:
			self.detected = True if pkt[0] == 1 else False
		print('binaryInfrared: ', self.name, pkt)
		
	def set_packet_stream(self, ps):
		ps.recv = self.on_recv
		self.ps = ps
		
	def run(self):
		if self.sensor_map == None:
			self.sensor_map = _core.sensors
		asyncio.ensure_future(self.loop())
