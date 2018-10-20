import platform
import importlib
from core.Util import *
class PathfinderService:
	def __init__(self):
		self.name = 'pathfinder'
		
		if platform.machine() == 'x86_64':
			from .pathfinder import Pathfinder_x86_64
			self.pathfinder = Pathfinder_x86_64.Pathfinder()
		else:
			from .pathfinder import Pathfinder_armv7l
			self.pathfinder = Pathfinder_armv7l.Pathfinder()
		
		
		
		self.loaded_ents=[]
	def run(self):
		# terrain restriction polygons
		s = max(self.core.robot_size)/2
		#  self.pathfinder.AddPolygon(polygon_from_rect([-1500,-1000,10,2000+100]),s)
		#  self.pathfinder.AddPolygon(polygon_from_rect([-1500,1000-10,3000+100,10]),s)
		#  self.pathfinder.AddPolygon(polygon_from_rect([1500,-1000,10,2000+100]),s)
		#  self.pathfinder.AddPolygon(polygon_from_rect([-1500,-1000,3000+100,10]),s)
		obsize = 100
		self.core.entities.add_entity('static','terrain',polygon_from_rect([-1500-obsize,-1000,obsize,2000+100]))
		self.core.entities.add_entity('static','terrain',polygon_from_rect([-1500,1000,3000+100,obsize]))
		self.core.entities.add_entity('static','terrain',polygon_from_rect([1500,-1000,obsize,2000+100]))
		self.core.entities.add_entity('static','terrain',polygon_from_rect([-1500,-1000-obsize,3000+100,obsize]))
		
		self.core.entities.on_remove_entity.append(self.on_ent_remove)
		self.core.entities.on_refresh_entity.append(self.on_refresh_entity)
	
	def export_cmds(self):
		#  self.core.export_cmd('pathfind', self.pathfind)
		pass
	
	def on_ent_remove(self, ent):
		if hasattr(ent, 'poly_id'):
			print('pathfinding removing ', ent.name, ent.poly_id)
			self.pathfinder.RemovePolygon(ent.poly_id)
			self.loaded_ents.remove(ent)
	
	def on_refresh_entity(self, ent):
		if hasattr(ent, 'poly_id'):
			self.pathfinder.RemovePolygon(ent.poly_id)
			int_polygon = [(int(pt[0]),int(pt[1])) for pt in ent.polygon]
			ent.poly_id = self.pathfinder.AddPolygon(int_polygon, max(self.core.robot_size)/2)
			ent.pf_poly = self.pathfinder.GetPolygon(ent.poly_id)
		
	def prepare_pathfinder(self):
		self.process_ents(self.core.entities.get_entities('static'))
		
	def process_ents(self, ents):
		added=False
		for ent in ents:
			if ent not in self.loaded_ents:
				added=True
				int_polygon = [(int(pt[0]),int(pt[1])) for pt in ent.polygon]
				print('appnd poly:', ent.name, int_polygon)
				ent.poly_id = self.pathfinder.AddPolygon(int_polygon, max(self.core.robot_size)/2)
				ent.pf_poly = self.pathfinder.GetPolygon(ent.poly_id)
				self.loaded_ents.append(ent)
		if added:
			self.core.introspection.send_entities()
			
	def fix_path(self, path):
		if len(path) <= 2:
			if path:
					
				return path[1:]
				#  return path
			else:
				return path
		
		new_path = []
		for i in range(1, len(path)-1):
			#  if vec_length(sub_pt(self.core.position, path[i])):
			prev_vec = sub_pt(path[i], path[i-1])
			next_vec = sub_pt(path[i+1], path[i])
			#  if prev_vec
			if abs(vector_angle_diff(prev_vec, next_vec)) > math.radians(2):
				new_path.append(path[i])
		#  print('old',path, 'new', new_path)
		return new_path + [path[-1]]
		
	def pathfind(self, point):
		
		static_ents = self.core.entities.get_entities('static')
		dyn_ents = self.core.entities.get_entities('robot')
		
		self.process_ents(static_ents)
		self.process_ents(dyn_ents)
		path = self.pathfinder.Search(tuple(self.core.position), tuple(point))
		
		#  if path:
			#  path = path[1:]
		return path
