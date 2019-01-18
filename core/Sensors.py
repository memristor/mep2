from .Util import *
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
	# robot is looking in positive X axis direction
	def add_sensor_point(self, sensor_type, sensor_name, rel_start, rel_end, duration=100):
		p = SensorPoint(sensor_type, sensor_name, rel_start, rel_end, duration)
		pos=_core.get_position()
		pt=pos[:2]
		o=pos[2]
		abs1 = add_pt(pt, rel_start)
		abs2 = add_pt(rot_vec_deg(p.rel2, o), pt)
		p.abs1 = _core.transform.transform(abs1)
		p.abs2 = _core.transform.transform(abs2)
		if not is_in_rect(p.abs2, [-1500, -1000, 3000, 2000]):
			return
		self.sensor_data.append(p)
		_core.emit('sensor:new_pt', p)
		
	#  def get_sensor_data(self, sensor_name, timestamp=0):
		#  return list(filter(lambda x: sensor_name == x.sensor_name))
		
	def get_sensor_data(self, sensor_name, count, timestamp=0):
		#  return list(filter(lambda x: sensor_name == x.sensor_name))
		return list(filter(lambda x: sensor_name == x.name, self.sensor_data[-count:]))
