import binascii
from .const_motion import *
from .convert import *

from core.network.packet.PacketStream import *
from core.Util import *
from math import sqrt,modf
import time

status_idle = 'I'

def vec_length(x,y):
	return sqrt(x**2+y**2)
	
def P_cmd(p):
	print(chr(p[0]) + " (" + str(l16(p, 1)) + ", " + str(l16(p, 3)) + ")  angle: " + str(l16(p, 5))) 
	
def nice_hex(s, spaces=4):
	h = binascii.hexlify(s).decode('ascii')
	return ' '.join([h[i:i+spaces] for i in range(0, len(h)-(len(h)%spaces)+spaces, spaces)])
	
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
		ps.recv = self.on_recv
		self.ps = ps
	
	def fix_glitch(self):
		print('fixing glitch')
		
		if self.future:
			self.future.runable.redo()
	
	
	def on_recv(self, pkt):
		if chr(pkt[0]) == 'P':
			s = chr(pkt[1])
			x = l16(pkt, 2)
			y = l16(pkt, 4)
			a = l16(pkt, 6)
			#  print(self.core.look_vector())
			#  if self.tol > 0 and point_distance([x,y], self.point) < self.tol:
				#  self.resolve(True)
				
			#  print(pkt)
			self.position = [x,y,a]
			self.core.set_position(x,y,a)
			self.core.state['state'] = s
			
			#  if self.core.state['state2'] != self.core.state['state'] and self.core.state['state'] in ('I','E'):
				#  self.timeout = self.core.loop.call_later(0.2, self.fix_glitch)
				
			if s == 'I' and self.future and (time.monotonic() - self.future.time) > 0.05:
				print('glitch resolved')
				#  self.future.runable.redo()
				self.resolve(1)
				
		#  print(pkt)
		if chr(pkt[0]) == 'p':
			status = chr(pkt[1])
			self.core.state['state2'] = status
			
			if status == 'I':
				self.core.service_manager.emit('idle')
				if self.timeout:
					self.timeout.cancel()
				self.resolve(True)
				#  print('should resolve')
			elif status == 'S':
				print('stuck')
				self.core.service_manager.emit('stuck')
			elif status == 'E':
				print('motion got error')
				pass
		elif chr(pkt[0]) == 'C' and len(pkt) >= 6+1:
			print(nice_hex(pkt))
			self.resolve( conf_bytes_to_float(pkt[1:]) )
	
	@asyn2
	def tolerance(self,t):
		self.tol = t

	def resolve(self, v=True):
		if self.future:
			self.future.set_result(v)
			self.future = None
			print('motion resolved')

	def send(self, x):
		if self.disabled:
			return
		if self.debug:
			print(nice_hex(x))
		self.ps.send(x)
	
	@asyn2
	def send_cmd(self, x):
		self.send(x)
			
	def resume(self):
		pass
	
	def curve_cmd(self, x,y,alpha,oa,o):
		self.send(b'Q' + pack(x) + pack(y) + pack(alpha) + pack(oa) + uchr(to_uchar(o)))
	
	def move_to_cmd(self, x,y,r=100,o=1):
		self.send(b'N' + pack(x) + pack(y) + uchr(to_uchar(o)) + pack(r))
		
	def goto_cmd(self, x,y,r=100,o=1):
		self.send(b'G' + pack(x) + pack(y) + uchr(0) + uchr(to_uchar(o)))
		
	def turn_cmd(self, o):
		self.send(b'T' + pack(o))
		
	def stop_cmd(self):
		self.send(b'S')
	
	def export_cmds(self):
		#  print('exp cmd')
		self.core.export_cmd('goto', self.goto)
		self.core.export_cmd('speed', self.speed)
		self.core.export_cmd('curve', self.curve)
		self.core.export_cmd('forward', self.forward)
		self.core.export_cmd('absrot', self.absrot)
		self.core.export_cmd('turn', self.turn)
		self.core.export_cmd('move', self.move)
		self.core.export_cmd('stop', self.stop)
		self.core.export_cmd('conf_set', self.conf_set)
		self.core.export_cmd('conf_get', self.conf_get)
		self.core.export_cmd('setpos', self.setpos)
		self.core.export_cmd('softstop', self.softstop)
		self.core.export_cmd('send', self.send_cmd)
		self.core.export_cmd('tol', self.tolerance)
		
	def set_direction(self, d):
		self.core.state['direction'] = d
		
	@asyn
	def speed(self, s):
		self.send(b'V' + uchr(s))
		self.resolve(1)

	@asyn
	def forward(self, dist):
		print('\x1b[33m forward: \x1b[0m', dist)
		self.intr()
		self.send(b'D' + pack(dist) + bytes([0]))
		self.set_direction( 1 if dist > 0 else -1 )
		#  self.goal_position = self.core.position[0]
	
	def intr(self):
		self.send(b'i')
		return
		
	def fullstop(self):
		self.send(b'i')
		self.send(b's')
		self.disabled = True
		
	@asyn
	def move(self, x,y,r=100,o=1):
		print('\x1b[33m moving to: \x1b[0m', x, y)
		self.intr()
		self.point = [x,y]
		self.move_to_cmd(x,y,r,o)

	@asyn
	def goto(self, x,y,o=1):
		print('goto: ', x, y)
		self.intr()
		self.point = [x,y]
		
		if o == 0:
			d = dot(sub_pt(self.point, self.core.position), self.core.look_vector())
			o = 1 if d > 0 else -1
		self.goto_cmd(x,y,0,o)
		self.set_direction(1 if o >= 1 else -1)
	
	@asyn2
	def softstop(self):
		self.future = None
		self.send(b's')
	
	@asyn
	def absrot(self, a):
		print('absrot', a)
		self.send(b'A' + pack(a))
	
	@asyn
	def curve(self, x,y,alpha,oa,d):
		self.intr()
		self.curve_cmd(x,y,alpha,oa,d)
	
	@asyn
	def turn(self, o):
		print('turn: ', o)
		self.last_cmd
		self.intr()
		self.turn_cmd(o)
	
	@asyn
	def stop(self):
		self.intr()
		self.stop_cmd()
	
	@asyn
	def setpos(self, x=None,y=None,o=None):
		new=[x,y,o]
		p = list(self.position)
		for i in range(3):
			if new[i] != None:
				p[i] = new[i]
		self.send(b'I' + pack(p[0]) + pack(p[1]) + pack(p[2]))
		self.core.set_position(*p)
		self.future.set_result(1)

	def conf_list(self):
		print('bytes: ', config_bytes)
		print('ints: ', config_ints)
		print('floats: ', config_floats)

	def conf_get_key(self, c):
		if c in config_bytes:
			return config_bytes.index(c)
		elif c in config_ints:
			return config_ints.index(c) + len(config_bytes)
		elif c in config_floats:
			return config_floats.index(c) + len(config_bytes) + len(config_ints)
		else: 
			return False
			
	@asyn
	def conf_set(self, c,v, dec=4):
		if c in config_ints:
			self.send(b'c' + uchr(len(config_bytes) + config_ints.index(c)) + conf_float_to_bytes(v,0))
		elif c in config_bytes:
			self.send(b'c' + uchr(config_bytes.index(c)) + conf_float_to_bytes(v,0))
		elif c in config_floats:
			fv = float(v)
			if fv == 0:
				dec = 0
			else:
				dec = 9 - ( int(log10(abs(fv))) + 1 )
			self.send(b'c' + uchr(len(config_bytes) + len(config_ints) + config_floats.index(c)) + conf_float_to_bytes(fv, dec))
		else:
			self.resolve(False)
			return False
		self.resolve(True)
		return True

	def run(self):
		self.core.state['state2'] = 'I'
		self.core.state['state'] = 'I'
	@asyn
	def conf_get(self, c):
		self.send(b'C' + uchr(self.conf_get_key(c)))
