
class BasicSensorProcessor:
	def __init__(self, sensor_map=None, entity_map=None):
		if sensor_map == None:
			import core.Core
			self.sensor_map = core.Core.Core().sensors
		else:
			self.sensor_map = sensor_map
		
	def run(self):
		pass
