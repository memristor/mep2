from core.Util import *
class PathfinderService:
	def __init__(self):
		self.name = 'pathfinder'
		
		#TODO: add auto compilation if needed
		import platform
		if platform.machine() == 'x86_64':
			from .pathfinder import Pathfinder_x86_64
			self.pathfinder = Pathfinder_x86_64.Pathfinder()
		else:
			from .pathfinder import Pathfinder_armv7l
			self.pathfinder = Pathfinder_armv7l.Pathfinder()
		
		self.loaded_ents=[]
	def run(self):
		# terrain restriction polygons
		s = max(_core.robot_size)/2
		obsize = 100
		playing_area_constaint = [ [-1500-obsize, -1000, obsize, 2000+obsize], [-1500, 1000, 3000+obsize, obsize], 
									[1500, -1000, obsize, 2000+100], [-1500, -1000-obsize, 3000+obsize, obsize] ]
		for rect in playing_area_constaint:
			poly = polygon_from_rect(rect)
			# self.pathfinder.AddPolygon(poly,s)
			_core.entities.add_entity('static','terrain', poly)
		
		_core.entities.on_remove_entity.append(self.on_ent_remove)
		_core.entities.on_refresh_entity.append(self.on_refresh_entity)
	
	def export_cmds(self):
		#  _core.export_cmd('pathfind', self.pathfind)
		pass
	
	def on_ent_remove(self, ent):
		if hasattr(ent, 'poly_id'):
			# print('pathfinding removing ', ent.name, ent.poly_id)
			self.pathfinder.RemovePolygon(ent.poly_id)
			self.loaded_ents.remove(ent)
	
	def on_refresh_entity(self, ent):
		if hasattr(ent, 'poly_id'):
			self.pathfinder.RemovePolygon(ent.poly_id)
			int_polygon = [(int(pt[0]),int(pt[1])) for pt in ent.polygon]
			ent.poly_id = self.pathfinder.AddPolygon(int_polygon, max(_core.robot_size)/2)
			ent.pf_poly = self.pathfinder.GetPolygon(ent.poly_id)
		
	def prepare_pathfinder(self):
		self.process_ents(_core.entities.get_entities('static'))
		
	def process_ents(self, ents):
		added=False
		for ent in ents:
			if ent not in self.loaded_ents:
				added=True
				int_polygon = [(int(pt[0]),int(pt[1])) for pt in ent.polygon]
				# print('appnd poly:', ent.name, int_polygon)
				ent.poly_id = self.pathfinder.AddPolygon(int_polygon, max(_core.robot_size)/2)
				ent.pf_poly = self.pathfinder.GetPolygon(ent.poly_id)
				self.loaded_ents.append(ent)
		if added:
			_core.introspection.send_entities()
			
	def fix_path(self, path):
		if len(path) <= 2:
			return path
		new_path = []
		for i in range(1, len(path)-1):
			prev_vec = sub_pt(path[i], path[i-1])
			next_vec = sub_pt(path[i+1], path[i])
			if abs(vector_angle_diff(prev_vec, next_vec)) > math.radians(2):
				new_path.append(path[i])
		return new_path + [path[-1]]
		
	def pathfind(self, point):
		
		static_ents = _core.entities.get_entities('static')
		dyn_ents = _core.entities.get_entities('robot')
		
		self.process_ents(static_ents)
		self.process_ents(dyn_ents)
		path = self.pathfinder.Search(tuple(_core.get_position()[:2]), tuple(point))

		return path
