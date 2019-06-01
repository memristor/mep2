from core.Util import polygon_square_around_point, point_distance
class LidarProcessor:
	def __init__(self, name='lidar processor'):
		self.name = name
		State.conf.lidar_duration = 2

	def on_new_pt(self, pt):
		if pt.type != 'lidar': return

		if not _core.is_dangerous(pt.abs1, pt.abs2):
			return
		
		ents = _core.entities.get_entities()
		poly = polygon_square_around_point(pt.abs2, 330)
		for ent in ents:
			if point_distance( ent.point, pt.abs2 ) < 200:
				if ent.type == 'robot' or ent.type == 'friendly_robot':
					ent.refresh(poly)
					return
		_core.entities.add_entity('robot', 'robot', poly, point=pt.abs2, duration=State.conf.lidar_duration, source='lidar') 
		
	def run(self):
		_core.listen('sensor:new_pt', self.on_new_pt)
