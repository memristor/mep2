from .Util import Event, rot_vec_deg, is_in_rect
from operator import add
class SensorPoint:
	def __init__(self, sensor_type, sensor_name, start_point, end_point, duration):
		self.type = sensor_type
		self.name = sensor_name
		self.rel1 = start_point
		self.rel2 = end_point
		self.abs1 = None
		self.abs2 = None
		self.duration = duration
		
		
class Sensors:
	def __init__(self):
		self.sensor_data = []
		self.on_new_point = Event()
	
	#
	# relative position is:
	#  ^
	#  y
	#  |
	# ROBOT> -x->
	#
	#  def add_sensor_data(self, sensor_name, point, duration=100):
		#  p = SensorPoint(sensor_name, point, duration)
		#  abs_pos = list(map(add, rot_vec_deg(p.rel_point, self.core.angle), self.core.position))
		#  p.abs_point = self.core.transform.transform(abs_pos)
		#  self.sensor_data.append( p )
		#  self.on_new_point(p)
		
	
	def add_sensor_point(self, sensor_type, sensor_name, rel_start, rel_end, duration=100):
		p = SensorPoint(sensor_type, sensor_name, rel_start, rel_end, duration)
		abs1 = list(map(add, self.core.position, rel_start))
		abs2 = list(map(add, rot_vec_deg(p.rel2, self.core.angle), self.core.position))
		p.abs1 = self.core.transform.transform(abs1)
		p.abs2 = self.core.transform.transform(abs2)
		#print(p.abs2)
		if not is_in_rect(p.abs2, [-1500, -1000, 3000, 2000]):
			return
		self.sensor_data.append(p)
		self.on_new_point(p)
		
	#  def get_sensor_data(self, sensor_name, timestamp=0):
		#  return list(filter(lambda x: sensor_name == x.sensor_name))
		
	def get_sensor_data(self, sensor_name, count, timestamp=0):
		#  return list(filter(lambda x: sensor_name == x.sensor_name))
		return list(filter(lambda x: sensor_name == x.name, self.sensor_data[-count:]))
