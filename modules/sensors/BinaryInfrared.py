from core.Util import rot_vec_deg
from operator import add
import asyncio
class BinaryInfrared:
	def __init__(self, name, sensor_position, sensor_vector, sensor_map=None):
		self.ps = None
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
				#print('adding')
				self.sensor_map.add_sensor_point('infrared', self.name, self.sensor_position, 
					list(map(add, self.sensor_position, self.sensor_vector)))
		
	def on_recv(self, pkt):
		if self.enabled:
			if pkt[0] == 1:
				self.detected = True
			else:
				self.detected = False
		print('binaryInfrared: ', self.name, pkt)

		
	def set_packet_stream(self, ps):
		ps.recv = self.on_recv
		self.ps = ps
		
	def run(self):
		if self.sensor_map == None:
			self.sensor_map = self.core.sensors
		asyncio.ensure_future(self.loop())
