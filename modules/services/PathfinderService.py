from core.Util import *
from .pathfinder_cpp import pathfinder
class PathfinderService:
	def __init__(self, export=False):
		self.name = 'pathfinder'
		self.pathfinder = pathfinder.Pathfinder()
		self.inflation = 10
		self.d=[]
		if export: self.export_cmds()
		
	def run(self):
		# terrain restriction polygons
		s = max(_core.robot_size)/2
		obsize = 35
		playing_area_constaint = [ [-1500-obsize, -1000, obsize, 2000+obsize], [-1500, 1000, 3000+obsize, obsize], 
									[1500, -1000, obsize, 2000+100], [-1500, -1000-obsize, 3000+obsize, obsize] ]
		for rect in playing_area_constaint:
			poly = polygon_from_rect(rect)
			# self.pathfinder.AddPolygon(poly,s)
			_core.entities.add_entity('static','terrain', poly)
		_core.listen('entity:remove',self.on_ent_remove)
		_core.listen('entity:refresh',self.on_refresh_entity)
		# _core.listen('strategy:done', self.save_logs)
		self.prepare_pathfinder()
	
	def export_cmds(self):
		_core.export_ns('')
		_core.export_cmd('testpath', self.pathfind)
		_core.export_cmd('pathfind', self.cmd_pathfind)
	
	# @_core.do(_atomic=1)
	def cmd_pathfind(self, x,y,o=1):
		# t=_e._ref()
		# def on_entity(ent):
			# pos=_core.get_position()[:2]
			# if is_intersecting_poly([x,y], pos, ent.polygon):
				# _e.r.softstop(_future=None)
				# _e.sleep(1)
				# print('redoing path', [x,y], pos, ent.polygon)
				# if point_distance(pos, ent.point) < 300:
					# _e._redo(ref=t)
				
		#_e._listen('entity:new', on_entity)
		#_e._listen('entity:refresh', on_entity)
		
		print('pathfinding ', x,y)
		path = self.pathfind([x,y])
		# print('pathfinding took:', dif())
		# path = pathfinder.fix_path(path)
		if not path:
			print('!! no path !!')
			_e._print('no path: ', x,y)
			# _e.sleep(2)
			# _e._goto('redo')
			# _e._redo()
			# _e._task_suspend()
			return False
		else:
			print('found path: ', path)
		for pt in path:
			_e.r.goto(*pt,0)
			# _e.r.diff_drive(*pt,0)
			# _e.r.move(*pt,150,0)
		return True
	
	def on_ent_remove(self, ent):
		if hasattr(ent, 'poly_id'):
			# print('pathfinding removing ', ent.name, ent.poly_id)
			self.pathfinder.RemovePolygon(ent.poly_id)
			print('pathfinding service removing polygon', ent.name, ent.poly_id)
			del ent.poly_id
	
	def on_refresh_entity(self, ent):
		if hasattr(ent, 'poly_id'):
			self.pathfinder.RemovePolygon(ent.poly_id)
			del ent.poly_id
		
	def prepare_pathfinder(self):
		self.process_ents(_core.entities.get_entities('static'))
		
	def process_ents(self, ents):
		added=False
		for ent in ents:
			if not hasattr(ent, 'poly_id'):
				added=True
				int_polygon = [(int(pt[0]),int(pt[1])) for pt in ent.polygon]
				# print('appnd poly:', ent.name, int_polygon)
				ent.poly_id = self.pathfinder.AddPolygon(int_polygon, max(_core.robot_size)/2 + (self.inflation*0.4 if ent.type == 'static' else self.inflation))
				ent.pf_poly = self.pathfinder.GetPolygon(ent.poly_id)
		if added:
			_core.introspection.send_entities()
			
	def fix_path(self, path):
		if len(path) <= 2: return path
		new_path = []
		for i in range(1, len(path)-1):
			prev_vec = sub_pt(path[i], path[i-1])
			next_vec = sub_pt(path[i+1], path[i])
			if abs(vector_angle_diff(prev_vec, next_vec)) > math.radians(10):
				new_path.append(path[i])
		return new_path + [path[-1]]
	
	
	def log(self, path):
		static_ents = _core.entities.get_entities('static')
		dyn_ents = _core.entities.get_entities('robot')
		o={'poly':[], 'pf_polys':[], 'path':path, 'position':_core.get_position(), 
			'robot_poly':polygon_rotate( polygon_square_around_point(_core.get_position()[:2], _core.robot_size), _core.get_position()[2] )
			}
		for ent in static_ents+dyn_ents:
			o['pf_polys'].append(ent.pf_poly if hasattr(ent, 'poly_id') else [])
			o['poly'].append(ent.polygon)
		self.d.append(o)
		
	def save_logs(self):
		print('saving logs')
		import json
		with open('paths-' + _core.robot + '.json', 'w') as f:
			f.write( json.dumps( self.d, indent=2 ) )
	

	def pathfind(self, point):
		ents = _core.entities.get_entities(['static', 'pathfind', 'robot'])
		self.process_ents(ents)
		path = self.pathfinder.Search(tuple(_core.get_position()[:2]), tuple(point))
		if path:
			path = path[1:]
		print('pf:', path)
		# if path: self.log(path)
		return path
