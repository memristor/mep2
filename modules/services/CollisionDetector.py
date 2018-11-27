import asyncio
from core.ServiceManager import Emitter
from core.Util import *
import math

class CollisionService(Emitter):
	def __init__(self, *a):
		super().__init__(*a)

DANGER = 'danger'
SAFE = 'safe'
	
class CollisionDetector:
	def __init__(self, wait_time=1, det_distance=100, det_angle=30, size=[-1500, -1000, 3000, 2000]):
		self.name = 'CollisionDetectorService'
		self.det_distance = det_distance
		self.future = None
		self.wait_time = wait_time
		self.size = size
		self.det_angle = det_angle
		self.rects = []
		self.state = SAFE
	
	def release(self):
		self.future = None
		if self.state == SAFE: return
		self.state = SAFE
		self.evt.emit(self.state)
		
	def on_new_pt(self, pt):
		if self.state == DANGER or _core.state['direction'] * pt.rel2[0] < 0:
			return
			
		#print('new pt', pt.rel2)
		if _core.state['state'] == 'R':
			# print('turning')
			return
		
		if pt.type == 'lidar':
			#  print('is lidar')
			vlen = vector_length(pt.rel2)
			if  vlen > 400:
				return False
		
			if math.degrees( abs( vector_angle_diff(pt.rel2, [1,0]) ) ) > self.det_angle:
				return False
			
			if not is_in_rect(pt.abs2, add_pt(self.size, [100, 100, -200, -200])):
				return False
		
		if self.is_dangerous(pt):
			self.emit_danger()
			
	def emit_danger(self):
		if self.future is not None:
			self.future.cancel()
		self.future = _core.loop.call_later(self.wait_time, self.release)
		if self.state == DANGER: return
		self.state = DANGER
		self.evt.emit(self.state)
		
		
	def on_new_entity(self, ent):
		if ent.type != 'robot':
			return
			
		if is_poly_in_pie_shape(ent.polygon, _core.get_position()[:2], _core.move_dir_vector(), self.det_distance, self.det_angle):
			self.emit_danger()
	
	def is_dangerous(self, pt):
		p1, p2 = pt.abs1, pt.abs2
		
		# its not dangerous when robot sensor hits some static obstacle
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
			
			# check entity map for collision
			for ent in robots:
				if point_distance(ent.point, _core.get_position()[:2]) < self.det_distance+200:
					if is_poly_in_pie_shape(ent.polygon, _core.get_position()[:2], _core.move_dir_vector(), self.det_distance, self.det_angle):
						self.emit_danger()

	def run(self):
		self.det_distance += max(_core.robot_size)
		_core.sensors.on_new_point.append(self.on_new_pt)
		_core.entities.on_new_entity.append(self.on_new_entity)
		self.evt = _core.service_manager.register('collision', CollisionService)
		asyncio.ensure_future(self.loop())
	
	
