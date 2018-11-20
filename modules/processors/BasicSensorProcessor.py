#TODO: add entity on entity map on collision
class BasicSensorProcessor:
	def __init__(self, sensor_map=None, entity_map=None):
		self.sensor_map = sensor_map or _core.sensors
		
	def run(self):
		pass
