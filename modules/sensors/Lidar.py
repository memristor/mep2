from core.Convert import l16
from core.Util import AABB, point_distance, add_pt, point_int
class Lidar:
	def __init__(self, tolerance=300, tune_angle=0, packet_stream=None):
		self.name = 'lidar'
		self.set_packet_stream(packet_stream)
		self.tune_angle = tune_angle
		self.points = 0
		self.sensor_position = [0,0]
		self.prevPoint = None
		self.tolerance = tolerance
		self.aabb = AABB()
		
	def on_recv(self,pkt):
		angle = l16(pkt, 0)
		dist = l16(pkt, 2)
		deg_angle = angle + self.tune_angle
		vector = rot_vec_deg([dist]*2, deg_angle)
		self.processPoint(vector)
		
	def set_packet_stream(self, ps):
		if not ps: return
		ps.recv = self.on_recv
		self.ps = ps
		
	def run(self):
		self.sensor_map = _core.sensors
	
	def processPoint(self, vec):
		pt = vec
		if self.points == 0:
			self.aabb = AABB(*pt)
			self.points += 1
			self.prevPoint = pt
		elif point_distance(pt, self.prevPoint) < self.tolerance:
			self.aabb.put(pt)
		else:
			if all((i < 300 for i in self.aabb.get_size())):
				self.sensor_map.add_sensor_point('lidar', self.name, self.sensor_position, add_pt(self.sensor_position, vec))
			self.points = 0
