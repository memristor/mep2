import binascii
from math import sqrt,modf,log10
import time
from core.Convert import *
from core.network.packet.PacketStream import *
from core.Util import *
from .const_motion import *

status_idle = 'I'

def simple_hash(v):
	h=5381
	for i in v:
		h = h*33 + ord(i)
	return int(h) & 0xffff

class Motion:
	def __init__(self, name='Motion', packet_stream=None):
		self.name = name
		self.debug = 0
		self.point = [1,2]
		self.tol = 0
		self.ps = None
		self.future=None
		self.last_cmd = None
		self.direction = 1
		self.position = [0,0,0]
		self.disabled = False
		self.timeout = False
		
		if packet_stream:
			self.set_packet_stream(packet_stream)
		
	def set_packet_stream(self, ps):
		self.ps = ps
		self.ps.recv = self.on_recv
	
	def fix_glitch(self):
		print('fixing glitch')
		if self.future:
			self.future.runable.redo()
	
	def on_recv(self, pkt):
		if chr(pkt[0]) == 'P':
			s,x,y,a = chr(pkt[1]), l16(pkt, 2), l16(pkt, 4), l16(pkt, 6)
			#  print(_core.look_vector())
			#  if self.tol > 0 and point_distance([x,y], self.point) < self.tol:
				#  self.resolve(True)
			self.position = [x,y,a]
			_core.set_position(x,y,a)
			_core.state['state'] = s
			
			#  if _core.state['state2'] != _core.state['state'] and _core.state['state'] in ('I','E'):
				#  self.timeout = _core.loop.call_later(0.2, self.fix_glitch)
			
			if s == 'I' and self.future and (time.monotonic() - self.future.time) > 0.05:
				print('glitch resolved')
				#  self.future.runable.redo()
				self.resolve(1)
				
		if chr(pkt[0]) == 'p':
			status = chr(pkt[1])
			_core.state['state2'] = status
			
			if status == 'I':
				_core.service_manager.emit('idle')
				if self.timeout:
					self.timeout.cancel()
				self.resolve(True)
				#  print('should resolve')
			elif status == 'S':
				print('stuck')
				_core.service_manager.emit('stuck')
			elif status == 'E':
				# print('motion got error')
				pass
		elif chr(pkt[0]) == 'C' and len(pkt) >= 6+1:
			# print(nice_hex(pkt))
			self.resolve( self.conf_bytes_to_float(pkt[1:]) )
	
	@_core.asyn2
	def tolerance(self,t):
		self.tol = t

	def resolve(self, v=True):
		if self.disabled:
			return
		if self.future:
			self.future.set_result(v)
			self.future = None
			# print('motion resolved')

	def send(self, x):
		if self.disabled:
			return
		if self.debug:
			print(nice_hex(x))
		self.ps.send(x)
	
	@_core.asyn2
	def send_cmd(self, x):
		self.send(x)
	
	def curve_cmd(self, x,y,alpha,oa,o):
		self.send(b'Q' + p16(x) + p16(y) + p16(alpha) + p16(oa) + p8(o))
	
	def move_to_cmd(self, x,y,r=100,o=1):
		self.send(b'N' + p16(x) + p16(y) + p8(o) + p16(r))
		
	def goto_cmd(self, x,y,r=100,o=1):
		self.send(b'G' + p16(x) + p16(y) + p8(0) + p8(o))
		
	def turn_cmd(self, o):
		self.send(b'T' + p16(o))
		
	def stop_cmd(self):
		self.send(b'S')
		
	def on_cancel(self):
		self.future = None
		print('on cancel')
	
	def export_cmds(self, namespace='r'):
		_core.export_ns(namespace)
		_core.export_cmd('goto', self.goto)
		_core.export_cmd('speed', self.speed)
		_core.export_cmd('curve', self.curve)
		_core.export_cmd('forward', self.forward)
		_core.export_cmd('absrot', self.absrot)
		_core.export_cmd('turn', self.turn)
		_core.export_cmd('move', self.move)
		_core.export_cmd('stop', self.stop)
		_core.export_cmd('conf_set', self.conf_set)
		_core.export_cmd('conf_get', self.conf_get)
		_core.export_cmd('setpos', self.setpos)
		_core.export_cmd('softstop', self.softstop)
		_core.export_cmd('send', self.send_cmd)
		_core.export_cmd('tol', self.tolerance)
		_core.export_cmd('tol', self.send_cmd)
		_core.export_ns('')
		
	def set_direction(self, d):
		_core.state['direction'] = d
		
	@_core.asyn2
	def speed(self, s):
		self.send(b'V' + p8(s))

	@_core.module_cmd
	def forward(self, dist):
		print(col.yellow, 'forward:', col.white, dist)
		self.intr()
		self.send(b'D' + p16(dist) + bytes([0]))
		self.set_direction( 1 if dist > 0 else -1 )
		#  self.goal_position = _core.position[0]
	
	def intr(self):
		self.send(b'i')
		return
		
	def fullstop(self):
		self.send(b'i')
		self.send(b's')
		self.disabled = True
		
	@_core.module_cmd
	def move(self, x,y,r=100,o=1):
		print(col.yellow, 'moving to:', col.white, x, y)
		self.intr()
		self.point = [x,y]
		self.move_to_cmd(x,y,r,o)

	@_core.module_cmd
	def goto(self, x,y,o=1):
		print('goto: ', x, y)
		self.intr()
		self.point = [x,y]
		
		if o == 0:
			d = dot(sub_pt(self.point, _core.get_position()[:2]), _core.look_vector())
			o = 1 if d > 0 else -1
		self.goto_cmd(x,y,0,o)
		self.set_direction(1 if o >= 1 else -1)
	
	@_core.asyn2
	def softstop(self):
		self.future = None
		self.send(b's')
	
	@_core.module_cmd
	def absrot(self, a):
		print('absrot', a)
		self.send(b'A' + p16(a))
	
	@_core.module_cmd
	def curve(self, x,y,alpha,oa,d):
		self.intr()
		self.curve_cmd(x,y,alpha,oa,d)
	
	@_core.module_cmd
	def turn(self, o):
		print('turn: ', o)
		self.last_cmd
		self.intr()
		self.turn_cmd(o)
	
	@_core.module_cmd
	def stop(self):
		self.intr()
		self.stop_cmd()
	
	@_core.asyn2
	def setpos(self, x=None,y=None,o=None):
		new=[x,y,o]
		p = list(self.position)
		for i in range(3):
			if new[i] != None:
				p[i] = new[i]
		self.send(b'I' + p16(p[0]) + p16(p[1]) + p16(p[2]))
		_core.set_position(*p)

	########## CONFIG ##########
	def conf_list(self):
		confs=config_bytes + config_ints + config_floats
		import textwrap
		print('\n'.join(textwrap.wrap('['+'] ['.join(confs)+']')))

	def conf_float_to_bytes(self, x, decimals=4):
		x *= pow(10, decimals)
		x = int(x)
		s = 1 if x < 0 else 0
		# x = abs(x) & 0xffffffff
		return p32(x) + bytes([s, decimals])
		
	def conf_bytes_to_float(self, x):
		num = l32(x,0)
		s = x[4]
		if s == 1:
			num = -num
		dec = float(x[5])
		return float(num) / pow(10, dec)
	
	def conf_get_key(self, c):
		if c in config_bytes:
			return config_bytes.index(c)
		elif c in config_ints:
			return config_ints.index(c) + len(config_bytes)
		elif c in config_floats:
			return config_floats.index(c) + len(config_bytes) + len(config_ints)
		else:
			return False
	
	use_hash=True
	
	@_core.module_cmd
	def conf_set(self, k, v, dec=4, _sim=False):
		if _sim:
			return 0
		self.future.val = 0
		if k in config_floats:
			fv = float(v)
			dec = 0 if fv == 0 else 9 - ( int(log10(abs(fv))) + 1 )
			v = fv
		key = p8(self.conf_get_key(k)) if not self.use_hash else p16(simple_hash(k))
		to_send = bytearray(self.conf_float_to_bytes(v,dec))
		if self.use_hash: del to_send[-2]
		cmd = b'c' if not self.use_hash else b'h'
		msg = cmd + key + bytes(to_send)
		self.send(msg)

	def run(self):
		_core.state['state2'] = 'I'
		_core.state['state'] = 'I'
		
	@_core.module_cmd
	def conf_get(self, k):
		key=p8(self.conf_get_key(k)) if not self.use_hash else p16(simple_hash(k))
		cmd = b'C' if not self.use_hash else b'H'
		msg = cmd + key
		self.send(msg)
