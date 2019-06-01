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
		self.disabled_entities = []
	def update_entity(self, entity_type, entity_name, polygon, point=None, duration=0):
		ent=self.get_entity_by_name(entity_name)
		if not ent:
			self.add_entity( entity_type, entity_name, polygon, point, duration )
		else:
			# print('refreshing ent', ent.name, ent.point)
			ent.refresh( polygon, point )
			
	def disable_entity(self, entity_name):
		ent=self.get_entity_by_name(entity_name)
		if ent:
			self.entities.remove(ent)
			self.disabled_entities.append(ent)
			print('disabling entity', entity_name, ent)
			_core.emit('entity:remove', ent)
		
	def enable_entity(self, entity_name):
		ent = next((i for i in self.disabled_entities if i.name == entity_name), None)
		if ent:
			print('enabling entity', entity_name, ent)
			self.disabled_entities.remove(ent)
			self.entities.append(ent)
			_core.emit('entity:new', ent)
	
	def remove_safe_zone(self, name):
		safe = next((i for i in self.safe_zones if i[0] == name), None)
		self.safe_zones.remove(safe)
		
	def add_safe_zone(self, name, polygon):
		self.safe_zones.append((name,polygon))
	
	def add_entity(self, entity_type, entity_name, polygon, point=None, duration=0, source=''):
		e = Entity(entity_type, entity_name, point, polygon, duration)
		e.source = source
		point = e.point
		if entity_type == 'friendly_robot':
			friendly = self.get_entities(entity_type)
			if friendly:
				friendly[0].refresh(polygon, point)
				return friendly[0]
		
		if entity_type == 'robot':
			closest, dist = self.get_closest_entity_to_point(point, entity_type)
			if dist < 150:
				# print('refreshing')
				closest.refresh(polygon, point)
				return closest
		
		aabb = AABB.from_polygon(polygon)
		e.aabb = [] + point + aabb.get_size()
		e.id = self.last_id
		self.last_id += 1
		self.entities.append(e)
		_core.emit('entity:new', e)
		return e
		
	def get_entities(self, entity_type=None, last_time=0):
		self.refresh()
		if entity_type is not None:
			return list(filter(lambda x: x.type in entity_type if type(entity_type) is list else x.type == entity_type, self.entities))
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
		return self.get_entities_in_polygon(polygon_from_rect(rect))
		
	def get_entities_in_polygon(self, poly):
		return [i for i in self.entities if is_point_in_poly(i.point, poly) or is_poly_intersecting_poly(i.polygon, poly)]

	def get_entities_in_line(self, p1, p2):
		return [i for i in self.entities if is_intersecting_poly(p1, p2, i.polygon)]
		
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
