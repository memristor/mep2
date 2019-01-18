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
		_core.export_ns(namespace)
		_core.export_cmd('lift', self.lift)
		_core.export_cmd('lift_sw', self.lift_sw)
		_core.export_cmd('prepare_lift', self.prepare_lift)
		
		
		
	def initialize(self):
		self.motion.conf_set('regulator_mode', 0)
		self.motion.conf_set('encoder1', 0)
		self.motion.conf_set('setpoint1', 0)
		self.motion.send(b'i')
		self.motion.send(b'R')
		self.motion.conf_set('debug_encoders', 0)
		self.motion.conf_set('encoder1', 0)
		self.motion.conf_set('encoder1_max', -self.lift_max)
		self.motion.conf_set('speed1', 300)
		self.motion.conf_set('tol1', 300)
		self.motion.conf_set('tol2', 40)
		self.motion.conf_set('pid_lin1', 0.7)
		self.motion.conf_set('pid_lin2', 1.2)
		self.motion.conf_set('pid_i1', 0.3)
		self.motion.conf_set('pid_i2', 1.0)
		self.motion.conf_set('encoder2_max', self.l2+self.l2/2)
		self.motion.conf_set('encoder2', self.l2/2)
		self.motion.conf_set('setpoint2', self.l2/2)
		self.motion.conf_set('speed2', 35)
		self.motion.conf_set('regulator_mode', 1)
	
	def prepare_lift(self,_future):
		self.ready_future = _future
		self.motion.send(b'-')
		

	def lift(self,x,_future):
		if self.sim or self.lift_pos == x:
			_future.set_result(1)
			return
		self.lift_pos = x
		self.lift_future = _future
		self.motion.conf_set('setpoint1', -x*390480 - (47000 if x != 0 else 0))
	
	def lift_sw(self,_future=None):
		if self.sim:
			_future.set_result(1)
			return
		self.lift_future = _future
		self.motion.conf_set('setpoint1', -300000)
	
	def fullstop(self):
		self.disabled = True
	
	def resolve(self, v=True):
		if self.future:
			self.future.set_result(v)
			self.future = None
	
	def set_packet_stream(self, ps):
		self.ps = ps
		self.motion.set_packet_stream(ps)
		ps.recv = self.on_recv
