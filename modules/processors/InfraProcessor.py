from core.Util import polygon_square_around_point, point_distance
class InfraProcessor:
	def __init__(self, tune_angle=0):
		self.name = 'InfraredProcessor'
		self.tune_angle = tune_angle
		
	def on_new_pt(self, pt):
		if pt.type != 'infrared': return
		# print('infra processor', pt.type, pt.name, pt.rel1, pt.rel2)
		
		if not _core.is_dangerous(pt.abs1, pt.abs2):
			return
		# ents = _core.entities.get_entities()
		poly = polygon_square_around_point(pt.abs2, 200)
		# for ent in ents:
			# if point_distance( ent.point, pt.abs2 ) < 300:
				# if ent.type == 'robot' or ent.type == 'friendly_robot':
					# ent.refresh(poly)
				# return
		# _core.entities.add_entity('robot', 'robot', poly, point=pt.abs2, duration=3.5) 
		_core.entities.add_entity('robot', 'robot', poly, point=pt.abs2, duration=3.5)
		
	def run(self):
		_core.listen('sensor:new_pt', self.on_new_pt)
