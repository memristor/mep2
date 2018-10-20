from .Util import *
import time
gcore = None
class EntityPoint:
	def __init__(self, entity_type, entity_name, point, polygon, duration):
		self.type = entity_type
		self.name = entity_name
		#  self.point = point
		#  self.polygon = polygon # list of tuples [(x,y),(x,y),...]
		self.creation_duration = duration
		
		self.recreate(polygon, point)
		
	def recreate(self, polygon=None, point=None):
		if polygon:
			self.polygon = polygon
		if not point:
			self.point = polygon_midpoint(self.polygon)
		else:
			self.point = point
		self.creation_time = time.time()
		self.duration = self.creation_duration
		self.deleted = False
		
	def refresh(self, polygon=None, point=None):
		self.recreate(polygon, point)
		gcore.entities.on_refresh_entity(self)
		
class Entities:
	def __init__(self,core):
		global gcore
		self.entities = []
		self.on_new_entity = Event()
		self.on_refresh_entity = Event()
		self.on_remove_entity = Event()
		self.time = time.time()
		self.last_id = 0
		gcore = core
		
	def add_entity(self, entity_type, entity_name, polygon, point=None, duration=0):
		#  if not point:
			#  point = polygon_midpoint(polygon)
		e = EntityPoint(entity_type, entity_name, point, polygon, duration)
		point = e.point
		#  print(e.aabb, 's',aabb.get_size())
		
		if entity_type == 'friendly_robot':
			friendly = self.get_entities(entity_type)
			if friendly:
				friendly[0].refresh(polygon, point)
		
		if entity_type == 'robot':
			closest, dist = self.get_closest_entity_to_point(point, entity_type)
			if dist < 400:
				print('refreshing')
				closest.refresh(polygon, point)
				return
				
		aabb = AABB.from_polygon(polygon)
		e.aabb = [] + point + aabb.get_size()
		e.id = self.last_id
		self.last_id += 1
		self.entities.append(e)
		self.on_new_entity(e)
		#  print('newent', point)
		
	def get_entities(self, entity_type=None, last_time=0):
		self.refresh()
		if entity_type != None:
			ents = list(filter(lambda x: entity_type == x.type, self.entities))
		else:
			ents = self.entities
		#  print('get entities', ents)
		return ents
	
	def get_closest_entity_to_point(self, point, ent_type):
		ents = self.get_entities(ent_type)
		min_dist = 9999
		min_ent = None
		for ent in ents:
			dist = point_distance(point, ent.point)
			if dist < min_dist:
				min_dist = dist
				min_ent = ent
		return (min_ent, min_dist)
	
	def get_entities_in_arc(self, arc_center, center_angle, arc_size, filter_func=None):
		pass
		
	def get_entities_in_arc_around_robot(self, center_angle, arc_size, filter_func=None):
		pass
		
	def get_entities_in_rect(self, rect):
		return [i for i in self.entities if is_in_rect(i.point, rect)]
		
	def time_diff(self):
		t = time.time()
		past = self.time
		self.time = t
		return t-past
		
	def remove_entity(self, entity):
		entity.deleted = True
		print('removing entity')
		self.on_remove_entity(entity)
		self.entities.remove(entity)
		
	def refresh(self):
		to_remove = []
		dt = self.time_diff()
		for ent in self.entities:
			if ent.duration > 0:
				ent.duration -= dt
				if ent.duration <= 0:
					to_remove.append(ent)
		for i in to_remove:
			#  print('removing ent',i)
			self.remove_entity(i)
