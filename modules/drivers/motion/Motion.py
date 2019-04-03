import math
from core.Convert import *
from core.network.packet.PacketStream import *
from core.Util import *
from .const_motion import *

status_idle = 'I'

def simple_hash(v):
	h=5381
	for i in v: h = h*33 + ord(i)
	return int(h) & 0xffff

class Motion:
	def __init__(self, name='Motion', packet_stream=None):
		self.name = name
		self.debug = 0
		self.point = [999999,999999]
		self.tol = 0
		self.state_rep = 0
		self.ps = None
		self.future=None
		self.direction = 1
		self.disabled = False
		self.timeout = False
		self.wheel_distance = 282.5
		from core.State import StateBase
		self._accel = StateBase(.25)
		self._speed = StateBase(0x25)
		if packet_stream: self.set_packet_stream(packet_stream)
		
		
	def set_packet_stream(self, ps):
		self.ps = ps
		self.ps.recv = self.on_recv
		
	def print_cmd(self, name, *args):
		print('\x1b[33m',name+':','\x1b[0m', *args)
	
	def on_recv(self, pkt):
		
		if chr(pkt[0]) == 'P':
			if len(pkt) != 8: return
			s,x,y,a = chr(pkt[1]), l16(pkt, 2), l16(pkt, 4), l16(pkt, 6)
			self.tol = 0
			# print(_core.look_vector())
			if self.tol > 0 and point_distance([x,y], self.point) < self.tol:
				self.resolve(True)
			
			prev = _core.state['state']
			if prev != s:
				self.state_rep = 0
			else:
				self.state_rep += 1
				
			if self.state_rep >= 10 and _core.state['state2'] != s:
				ps = _core.state['state2']
				_core.state['state2'] = s
				if ps in 'MR' and prev == 'I':
					self.resolve(True)
					print('glitch resolved')
			
			_core.set_position(x,y,a)
			_core.state['state'] = s
			
		if chr(pkt[0]) == 'p':
			status = chr(pkt[1])
			print(status)
			prev = _core.state['state2']
			if _core.state['state2'] == status: return
			_core.state['state2'] = status
			self.state_rep = 0
			
			if status == 'I':
				_core.emit('motion:idle')
				if prev in 'MR': self.resolve(True)
			elif status == 'S':
				_core.emit('motion:stuck')
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
		if self.disabled: return
		if self.future:
			self.future.set_result(v)
			self.future = None
			# _core.state['state2'] = 'I'
			print('motion resolved')
			# _core.notify(self.name)

	def send(self, x):
		if self.disabled: return
		if self.debug: print(nice_hex(x))
		# if bigger than 8 bytes, send by using CAN packet extender protocol
		if len(x) > 8:
			left = len(x) - 1
			s = 1
			# \rTL 5
			l =  min(left,5)
			self.ps.send(b'\n' + bytes([x[0], left]) + x[s:s+l])
			left -= l
			s += l
			while left > 0:
				l =  min(left,7)
				self.ps.send(b'\r'+x[s:s+l])
				# print(s,left)
				left -= l
				s += l
		else:
			# send normal packet
			self.ps.send(x)
			
	
	@_core.asyn2
	def send_cmd(self, x): self.send(x)
		
	####### RAW COMMANDS #######
	def move_cmd(self, x,y,r=100,dir=1): self.send(b'N' + p16(x) + p16(y) + p16(r) + p8(dir))
	def goto_cmd(self, x,y,dir=1): self.send(b'G' + p16(x) + p16(y) + p8(dir))
	def absrot_cmd(self, a): self.send(b'A' + p16(a))
	def curve_cmd(self, x,y,alpha,dir=1): self.send(b'Q' + p16(x) + p16(y) + p16(alpha) + p8(dir))
	def turn_cmd(self, o): self.send(b'T' + p16(o))
	def stop_cmd(self): self.send(b'S')
	def motoroff_cmd(self): self.send(b's')
	def softstop_cmd(self): self.send(b't')
	def setpos_cmd(self, x=0,y=0,o=0): self.send(b'I' + p16(x) + p16(y) + p16(o))
	def intr_cmd(self): self.send(b'i')
	def forward_cmd(self, dist): self.send(b'D' + p16(dist))
	def diff_drive_cmd(self, x,y,alpha): self.send(b'L' +  p16(x) + p16(y) + p16(alpha))
	def motor_pwm_cmd(self, m1,m2): self.send(b'm' + p16(m1) + p16(m2))
	def const_speed_cmd(self, m1,m2): self.send(b'M' + p16(m1) + p16(m2))
	def curve_rel_cmd(self, r, alpha, dir=1): self.send(b'q' +  p16(r) + p16(alpha) + p8(dir))
	def speed_cmd(self, s): self.send(b'V' + p8(s))
	#############################
	
	def on_cancel(self):
		self.cancelling = True
		# self.softstop()
		# self.intr()
		# print('on cancel')
		# _core.state['state2'] = 'I'
		
	def export_cmds(self, namespace='r'):
		self.namespace = namespace
		_core.export_ns(namespace)
		_core.export_cmd('goto', self.goto)
		_core.export_cmd('speed', self.speed)
		_core.export_cmd('curve', self.curve)
		_core.export_cmd('curve_rel', self.curve_rel)
		_core.export_cmd('diff_drive', self.diff_drive)
		_core.export_cmd('forward', self.forward)
		_core.export_cmd('absrot', self.absrot)
		_core.export_cmd('turn', self.turn)
		_core.export_cmd('move', self.move)
		_core.export_cmd('stop', self.stop)
		_core.export_cmd('conf_set', self.conf_set)
		_core.export_cmd('conf_get', self.conf_get)
		_core.export_cmd('setpos', self.setpos)
		_core.export_cmd('stuckpos', self.stuckpos)
		_core.export_cmd('motoroff', self.motoroff)
		_core.export_cmd('softstop', self.softstop)
		_core.export_cmd('send', self.send_cmd)
		_core.export_cmd('tol', self.tolerance)
		_core.export_cmd('accel', self.accel)
		_core.export_cmd('intr', self.intr)
		_core.export_ns('')
		
	def set_direction(self, d):
		_core.state['direction'] = d
		
	@_core.asyn2
	def speed(self, s, _sim):
		self._speed.val = s
		if not _sim:
			self.accel(self._accel.val*1000, _sim)
			self.speed_cmd(s)
	
	def accel(self, a=None, _future=None, _sim=None):
		if a: self._accel.val = a/1000
		ret = self._accel.val*1000
		if _future:
			_future.set_result(ret)
		else:
			return ret
		if a and not _sim:
			self.conf_set('accel', a, _sim)
			self.conf_set('alpha', a, _sim)
	
	@_core.module_cmd
	def diff_drive(self,x,y,alpha):
		# TODO: add sim iface
		self.print_cmd('diff drive',x,y,alpha)
		self.diff_drive_cmd(x,y,alpha)
	
	@_core.module_cmd
	def forward(self, dist, _sim):
		if _sim:
			x1,y1,o1 = _core.get_position()
			L_dist = abs(dist)
			c_vmax=self._speed.val/256 # [m/s] 255 = 1m/s
			c_vmax *= 1000.0 # [mm/s]
			a=c_vmax/self._accel.val
			# calculate phase durations
			T1 = c_vmax/a; # speeding up
			L1 = a * T1**2 / 2.0
			
			T3 = T1; # slowing down
			L3 = L1
			L13 = L1+L3
			if L13 < L_dist: # can reach max speed
				L2 = L_dist - L13
				T2 = L2 / c_vmax
			else: # can't reach c_vmax
				T1 = math.sqrt(a * L_dist) / a
				T2 = 0
				T3=T1
			_core.set_position(*add_pt([x1,y1], _core.look_vector(dist)), o1)
			return T1+T2+T3
		
		self.print_cmd('forward',dist)
		self.forward_cmd(dist)
		self.set_direction( 1 if dist > 0 else -1 )
	
	@_core.asyn2
	def intr(self):
		self.intr_cmd()
		
	def fullstop(self):
		self.intr_cmd()
		self.motoroff_cmd()
		self.disabled = True
		
	@_core.module_cmd
	def move(self, x,y,r=100,o=1):
		self.print_cmd('moving to',x,y)
		x,y=int(x),int(y)
		self.point = [x,y]
		self.intr()
		self.move_cmd(x,y,r,o)

	@_core.module_cmd
	def goto(self, x,y,o=1,_sim=0):
		self.point = [x,y]
		
		# pick closest
		if o == 0:
			d = dot(sub_pt(self.point, _core.get_position()[:2]), _core.look_vector())
			o = 1 if d > 0 else -1
		
		if _sim:
			x1,y1,o1 = _core.get_position()
			p1=[x1,y1]
			p2=[x,y]
			angle = vector_orient(mul_pt(sub_pt(p2,p1), o))
			# print('angle: ', angle)
			dist = point_distance(p1, p2);
			T_turn = self.absrot(normalize_orient(angle), _sim)
			T_forward = self.forward(dist, _sim)
			_core.set_position(x,y,angle)
			return T_turn+T_forward
			
		self.print_cmd('goto',x, y, str(o) if o < 0 else '')
		self.goto_cmd(x,y,o)
		self.set_direction(1 if o >= 1 else -1)
	
	@_core.asyn2
	def softstop(self):
		self.intr()
		self.softstop_cmd()
		
	@_core.asyn2
	def motoroff(self):
		self.future = None
		self.motoroff_cmd()
	
	@_core.module_cmd
	def absrot(self, a, _sim=0):
		if _sim:
			o = normalize_orient(a-_core.get_position()[2])
			return self.turn(o,_sim)
		self.print_cmd('absrot', a)
		self.absrot_cmd(a)
	
	@_core.module_cmd
	def curve(self, x,y,alpha,dir=1, _sim=0):
		if _sim:
			r = int( _core.distance_to([x,y]) )
			t = 0
			if r > 0: 
				s = 1 if alpha > 0 else -1
				dir = 1 if dir > 0 else -1
				t=self.absrot( int( vector_orient( _core.vector_to([x,y]) ) + dir * -s * 90 ), _sim=1 )
			return self.curve_rel( r, alpha, dir, _sim=1 ) + t
		self.print_cmd('curve',x,y,alpha,dir)
		
		# test using subtask and combination of absrot and curve_rel
		'''
		def thr():
			nonlocal dir
			r = int(_core.distance_to([x,y]))
			t = 0
			if r > 0: 
				s = 1 if alpha > 0 else -1
				dir = 1 if dir > 0 else -1
				rot=int( vector_orient( _core.vector_to([x,y]) ) + dir * -s * 90 )
				_e.r.absrot(rot)
			_e.r.curve_rel(r, alpha, dir)
		_core.spawn(thr,future=self.future)
		'''
		
		self.curve_cmd(x,y, alpha, dir)
		
	@_core.module_cmd
	def curve_rel(self, r, angle, dir=1, _sim=0):
		if _sim:
			c_vmax=self._speed.val/256 * 1000
			c_omega = c_vmax
			g_accel=c_vmax/self._accel.val
			g_alpha=g_accel
			if r > self.wheel_distance:
				speed = c_vmax;
				accel = g_accel;
				L_dist = math.radians(angle) * r;
			else:
				speed = c_omega;
				accel = g_alpha;
				L_dist = math.radians(angle) * self.wheel_distance/2;
			
			T1 = T3 = speed / accel;
			L1 = accel * T1 * T1 / 2;
			
			if L1 > L_dist / 2:
				L1 = L_dist / 2;
				T1 = T3 = math.sqrt(2 * L1 / accel);
				T2 = 0;
			else:
				T2 = (L_dist - 2*L1) / speed;
			return T1+T2+T3
		self.print_cmd('curve rel', r, angle, dir)
		self.curve_rel_cmd(r, angle, dir)
	
	@_core.module_cmd
	def turn(self, o, _sim):
		if _sim:
			# Fi is not really angle here, but distance to travel, as circumference
			Fi_abs = abs(math.radians(o)*self.wheel_distance/2)
			omega = self._speed.val / 255 * 1000 # [mm/s]
			alpha = omega / self._accel.val
			T1 = T3 = omega/alpha
			Fi1 = alpha * T1**2 / 2
			if Fi1 > Fi_abs / 2:
				Fi1 = Fi_abs / 2
				T1 = T3 = math.sqrt(2 * Fi1 / alpha)
				T2 = 0
				# print('turn glitch')
			else:
				T2 = (Fi_abs - 2 * Fi1) / omega
				# print('turn times: ' , T1,T2,T3, '---', Fi_abs, Fi1)
			
			x,y,o1 = _core.get_position()
			_core.set_position(x,y,normalize_orient(o1+o))
			return T1+T2+T3
			
		self.print_cmd('turn', o)
		self.turn_cmd(o)
	
	@_core.module_cmd
	def stop(self):
		self.intr()
		self.stop_cmd()
	
	@_core.asyn2
	def setpos(self, x=None,y=None,o=None,_sim=0):
		new=[x,y,o]
		p = list(_core.get_position())
		for i in range(3):
			if new[i] != None: p[i] = int(new[i])
		if not _sim:
			self.print_cmd('setpos', *p)
			self.setpos_cmd(*p)
		_core.set_position(*p)
	
	@_core.do
	def stuckpos(self, forw=1, x=None,y=None,o=None,_sim=0):
		p=r.conf_set('enable_stuck', 1)
		@_e._on('motion:stuck')
		def on_stuck():
			_goto('stuckpos_label', ref=p)
		r.forward(forw * 500)
		_e._L('stuckpos_label')
		_e.setpos(x=x, y=y, o=o)
	
	def run(self):
		_core.state['state2'] = 'I'
		_core.state['state'] = 'I'
		# _core.init_task(lambda: (self.intr(), self.setpos(0,0,0)))
	
	############# CONFIG #############
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
	
	@_core.asyn2
	def conf_set(self, k, v, dec=4):
		if k in config_floats:
			fv = float(v)
			dec = max(0, 0 if fv == 0 else 9 - ( int(math.log10(abs(fv))) + 2 ))
			v = fv
		key = p8(self.conf_get_key(k)) if not self.use_hash else p16(simple_hash(k))
		to_send = bytearray(self.conf_float_to_bytes(v,dec))
		if self.use_hash: del to_send[-2]
		cmd = b'c' if not self.use_hash else b'h'
		msg = cmd + key + bytes(to_send)
		self.send(msg)

	@_core.module_cmd
	def conf_get(self, k):
		key=p8(self.conf_get_key(k)) if not self.use_hash else p16(simple_hash(k))
		cmd = b'C' if not self.use_hash else b'H'
		msg = cmd + key
		self.send(msg)
	#####################################

	
		
