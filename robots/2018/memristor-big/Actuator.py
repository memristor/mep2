from modules.drivers.motion.Motion import Motion
from core.network.Splitter import *
import time
class Actuator:
	def __init__(self,sim=False):
		self.name = 'big-actuator'
		self.l2 = 34768
		self.lift_max=1260000
		if not sim:
			from core.network.Uart import *
			uart = Uart() if not sim else None
			spl=Splitter(packet_stream)
			self.motion = Motion(name='Actuator motion board', packet_stream=spl.get())
			_core.add_module([uart,self.motion])
			spl.get().recv=self.on_recv
		self.min_time = 0.0
		self.sim = sim
		self.rot_pos = 2
		self.lift_pos = 0
		self.rot_future = None
		self.lift_future = None
		self.disabled = False
		self.export_cmds()
		
	def run(self):
		pass
		
	def on_recv(self, pkt):
		#  print(pkt)
		
		if pkt[0] == ord('X'):
			print('X')
			if self.ready_future:
				self.ready_future.set_result(1)
				
		if pkt[0] == 0x40 and self.rot_future:
			self.rot_future.set_result(1)
			self.rot_future = None
			print('rot done')
		elif pkt[0] == 0x21 and self.lift_future:
			self.lift_future.set_result(1)
			self.lift_future = None
			print('lift done')
	
	def export_cmds(self, namespace=''):
		_core.export_ns('a')
		_core.export_cmd('rotate', self.rotate)
		_core.export_ns(namespace)
		_core.export_cmd('lift', self.lift)
		_core.export_cmd('lift_sw', self.lift_sw)
		
		def rotate(x):
			if not self.sim:
				_e.a.rotate(x)
			_e.sleep(0.2)
				
		_core.export_cmd('rotate', rotate)
		_core.export_cmd('prepare_lift', self.prepare_lift)
				
		def unload(n, first=False):
			if n == 1:
				_e.r.forward(58)
				if first:
					_e.lift(0)
				_e.pump(1,0)
				if first:
					_e.lift(1)
				_e.r.forward(-58)    
			elif n == 2:  
				_e.rotate(3)
				if first:
					_e.lift(0)
				_e.pump(2,0)
			elif n == 3:
				_e.rotate(1)
				if first:
					_e.lift(0)
				_e.pump(3,0)
			elif n == 4:
				_e.rotate(2)
				if first:
					_e.lift(0)
				_e.pump(5,0)
			if first:
				_e.lift(1)
			
		colors=['green','blue','orange','black']
		def check_side(side, combination):
			global colors
			if colors[side-1] in combination and \
			   colors[side] in combination and \
			   colors[(side+1)%len(colors)] in combination:
				   return True
			return False


		def get_side(combination):
			for i in range(4):
				if check_side(i,combination):
					return i

		# 2,4,3
		#get_side(combination)
		def get_pump_order(combination):
			global colors
			rot=get_side(combination)
			c=[colors[rot-1], colors[rot], colors[(rot+1)%4]]
			pumps=[2,4,3]
			return [pumps[c.index(i)] for i in combination]

		def get(col, combination):
			global colors
			colors=col
			print(col,combination)
			if 'yellow' in combination:
				h = list(filter(lambda x: x != 'yellow', combination))
				s=set(colors)-set(h)
				replacement=next(i for i in s)
				idx=combination.index('yellow')
				combination2 = list(combination)
				combination2[idx] = replacement
				rot=get_side(combination2)
				p=get_pump_order(combination2)
				p[idx] = 1
				return (rot, p)
			else:
				return (get_side(combination), get_pump_order(combination))
		def get_remaining_pump(p):
			return next(i for i in (set(range(1,5))-set(p)))
		
		def pick():
			_e.lift(0)
			_e.pump(0,1)
			_e.sleep(0.2)
			_e.lift(1)
			
		_core.export_ns(namespace)
		_core.export_cmd('unload', unload)
		_core.export_cmd('get', get)
		_core.export_cmd('get_remaining_pump', get_remaining_pump)
		_core.export_cmd('pick', pick)
		
		def build_cubes(color):
			with _e.disabled('collision'):
				for i in enumerate(color):
					_e.lift(max(1, i[0]))
					_e.unload(i[1],i[0] == 0)
				_e.lift(3)
				_e.unload(_e.get_remaining_pump(color))

		
		_core.export_cmd('build_cubes', build_cubes)
		
		
	def initialize(self):
		self.motion.conf_set('linear_mode', 0)
		self.motion.conf_set('encoder1', 0)
		self.motion.conf_set('setpoint1', 0)
		self.motion.send(b'i')
		self.motion.send(b'R')
		self.motion.conf_set('debug_encoders', 0)
		#  self.motion.conf_set('left_motor_speed_limit', 3200)
		self.motion.conf_set('encoder1', 0)
		self.motion.conf_set('encoder1_max', -self.lift_max)
		self.motion.conf_set('speed1', 300)
		self.motion.conf_set('tol1', 300)
		self.motion.conf_set('tol2', 40)
		self.motion.conf_set('pid_lin1', 0.7)
		self.motion.conf_set('pid_lin2', 1.2)
		self.motion.conf_set('pid_i1', 0.3)
		self.motion.conf_set('pid_i2', 1.0)
		#  self.motion.conf_set('right_motor_speed_limit', 3200)
		self.motion.conf_set('encoder2_max', self.l2+self.l2/2)
		self.motion.conf_set('encoder2', self.l2/2)
		self.motion.conf_set('setpoint2', self.l2/2)
		self.motion.conf_set('speed2', 35)
		self.motion.conf_set('linear_mode',1)
	
	def prepare_lift(self,_future):
		self.ready_future = _future
		self.motion.send(b'-')
		
	def rotate(self, x, _future=None):
		if self.rot_pos == x:
			_future.set_result(1)
			return
		print('rot start')
		self.rot_pos = x
		self.rot_future = _future
		self.motion.conf_set('setpoint2', (self.l2/2) * (3-x))
	
	def lift(self,x,_future):
		if self.sim or self.lift_pos == x:
			_future.set_result(1)
			return
		print('lift start')	
		self.lift_pos = x
		self.lift_future = _future
		self.motion.conf_set('setpoint1', -x*390480 - (47000 if x != 0 else 0))
	
	def lift_sw(self,_future=None):
		if self.sim:
			_future.set_result(1)
			return
		print('lift start')	
		self.lift_future = _future
		self.motion.conf_set('setpoint1', -300000)
	
	def fullstop(self):
		print('actuator fullstop')
		#self.motion.
		#self.motion.conf_set('linear_mode', 0)
		self.disabled = True
	
	def resolve(self, v=True):
		if self.future:
			self.future.set_result(v)
			self.future = None
	
	def set_packet_stream(self, ps):
		self.ps = ps
		self.motion.set_packet_stream(ps)
		ps.recv = self.on_recv
