from core.Util import polygon_square_around_point, point_distance
class LidarProcessor:
	
	def __init__(self, tune_angle=0):
		self.name = 'lidar'
		self.tune_angle = tune_angle
		
	def on_new_pt(self, pt):
		if pt.type != 'lidar':
			return

		ents = self.core.entities.get_entities()
		#  print('on new pt')
		poly=polygon_square_around_point(pt.abs2, 500)
		for ent in ents:
			#  print(ent.point)
			if point_distance( ent.point, pt.abs2 ) < 300:
				if ent.type == 'robot' or ent.type == 'friendly_robot':
					ent.refresh(poly)
				return
				
			#  if friendly and point_distance(friendly[0].point, ent.point) < 300:
						#  continue
		self.core.entities.add_entity('robot', 'robot', poly, point=pt.abs2, duration=3.5) 
		
	def run(self):
		self.core.sensors.on_new_point.append(self.on_new_pt)
		pass
