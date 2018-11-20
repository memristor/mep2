import asyncio
from core.ServiceManager import Emitter
from core.Util import *
import math

class CollisionService(Emitter):
	def __init__(s, *a, **aa):
		super().__init__(*a,*aa)
	def on_new_listener(self, lst):
		pass
		
	def on_lose_listener(self, lst):
		pass
		
class CollisionDetector:
	def __init__(self, wait_time=1, det_distance=100, det_angle=30, size=[-1500, -1000, 3000, 2000]):
		self.name = 'CollisionDetectorService'
		self.det_distance = det_distance
		self.future = None
		self.wait_time = wait_time
		self.size = size
		self.det_angle = det_angle
		self.rects = []
	
	def release(self):
		self.evt.emit('safe')
		self.future = None
		
	def on_new_pt(self, pt):
		if _core.state['direction'] * pt.rel2[0] < 0:
			return
		#print('new pt', pt.rel2)
		if _core.state['state'] == 'R':
			print('turning')
			return
		
		if pt.type == 'lidar':
			#  print('is lidar')
			vlen = vector_length(pt.rel2)
			if  vlen > 400:
				return False
		
			if math.degrees( abs( vector_angle_diff(pt.rel2, [1,0]) ) ) > self.det_angle:
				return False
				
			if not is_in_rect(pt.abs2, [-1500+100, -1000+100, 3000-200, 2000-200]):
				return False
		
		if self.is_dangerous(pt):
			self.emit_danger()
		else:
			pass
			
	def emit_danger(self):
		if self.future != None:
			self.future.cancel()
		
		self.evt.emit('danger')
		self.future = _core.loop.call_later(self.wait_time, self.release)
		
	def on_new_entity(self, ent):
		if ent.type != 'robot':
			return
			
		if is_poly_in_pie_shape(ent.polygon, _core.get_position()[:2], _core.move_dir_vector(), self.det_distance, self.det_angle):
			self.emit_danger()
	
	def is_dangerous(self, pt):
		p1=pt.abs1
		p2=pt.abs2
		
		polygons = _core.entities.get_entities('static')
		for poly in polygons:
			if is_intersecting_poly(p1, p2, poly.polygon):
				# print('inters poly', p1,p2, poly.aabb)
				return False
		return True
	
	async def loop(self):
		while 1:
			await asyncio.sleep(0.3)
			if _core.state['state'] == 'R':
				continue
			robots = _core.entities.get_entities('robot')
			friendly = _core.entities.get_entities('friendly_robot')
			robots += friendly
			
			for ent in robots:
				if point_distance(ent.point, _core.get_position()[:2]) < self.det_distance+200:
					if is_poly_in_pie_shape(ent.polygon, _core.get_position()[:2], 
						_core.move_dir_vector(), self.det_distance, self.det_angle):
						self.emit_danger()
			
	def run(self):
		self.det_distance += max(_core.robot_size)
		_core.sensors.on_new_point.append(self.on_new_pt)
		_core.entities.on_new_entity.append(self.on_new_entity)
		self.evt = _core.service_manager.register('collision', CollisionService)
		asyncio.ensure_future(self.loop())
	
	
