from .Util import *
import time
class Entity:
	def __init__(self, entity_type, entity_name, point, polygon, duration):
		self.type = entity_type
		self.name = entity_name
		self.creation_duration = duration
		self.deleted = False
		self.recreate(polygon, point)
		
	def recreate(self, polygon=None, point=None):
		if polygon: self.polygon = polygon
		self.point = polygon_midpoint(self.polygon) if not point else point
		self.creation_time = time.time()
		self.duration = self.creation_duration
		self.deleted = False
		
	def refresh(self, polygon=None, point=None):
		self.recreate(polygon, point)
		_core.emit('entity:refresh', self)
		
class Entities:
	def __init__(self):
		self.entities = []
		self.time = time.time()
		self.last_id = 0
	
	def update_entity(self, entity_type, entity_name, polygon, point=None, duration=0):
		ent=self.get_entity_by_name(entity_name)
		if not ent:
			self.add_entity( entity_type, entity_name, polygon, point, duration )
		else:
			# print('refreshing ent', ent.name, ent.point)
			ent.refresh( polygon, point )
			
		
	def add_entity(self, entity_type, entity_name, polygon, point=None, duration=0):
		e = Entity(entity_type, entity_name, point, polygon, duration)
		point = e.point
		#print('add_entity: ', point)
		if entity_type == 'friendly_robot':
			friendly = self.get_entities(entity_type)
			if friendly:
				friendly[0].refresh(polygon, point)
		
		if entity_type == 'robot':
			closest, dist = self.get_closest_entity_to_point(point, entity_type)
			if dist < 150:
				# print('refreshing')
				closest.refresh(polygon, point)
				return
		
		aabb = AABB.from_polygon(polygon)
		e.aabb = [] + point + aabb.get_size()
		e.id = self.last_id
		self.last_id += 1
		self.entities.append(e)
		_core.emit('entity:new', e)
		
	def get_entities(self, entity_type=None, last_time=0):
		self.refresh()
		if entity_type is not None:
			return list(filter(lambda x: entity_type == x.type, self.entities))
		else:
			return self.entities
	
	def get_entity_by_name(self, entity_name):
		ents=self.get_entities()
		return next((i for i in ents if i.name == entity_name), None)
	
	def get_closest_entity_to_point(self, point, ent_type):
		ents = self.get_entities(ent_type)
		min_dist = 9999
		min_ent = None
		for ent in ents:
			dist = point_distance(point, ent.point)
			if dist < min_dist:
				min_dist, min_ent = dist, ent
		return (min_ent, min_dist)
	
	def get_entities_in_arc(self, arc_center, center_angle, arc_size, filter_func=None):
		pass
		
	def get_entities_in_arc_around_robot(self, center_angle, arc_size, filter_func=None):
		pass
		
	def get_entities_in_rect(self, rect):
		return [i for i in self.entities if is_in_rect(i.point, rect)]
		
	def get_entities_in_line(self, p1, p2):
		pass
		
	def time_diff(self):
		t = time.time()
		past = self.time
		self.time = t
		return t-past
		
	def remove_entity(self, entity):
		if type(entity) is str:
			entity = next((e for e in self.entities if entity == e.name), None)
			if entity is None: return
		entity.deleted = True
		_core.emit('entity:remove', entity)
		self.entities.remove(entity)
		
	def refresh(self):
		to_remove = []
		dt = self.time_diff()
		
		for ent in list(self.entities):
			if ent.duration > 0:
				ent.duration -= dt
				if ent.duration <= 0:
					self.remove_entity(ent)
