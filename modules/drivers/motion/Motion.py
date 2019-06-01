import math
from core.Convert import *
from core.network.packet.PacketStream import *
from core.Util import *
from .const_motion import *
from core.Future import Future

status_idle = 'I'
	
import core.CommandList as clist
class WithChain(clist.Block):
	def __init__(self, motion):
		super().__init__()
		self.motion = motion
	
	def __exit__(self, *exc):
		cmds = self.stop()
		
		cut_at = 0
		for i,cmd in enumerate(reversed(cmds.commands)):
			if cmd.name[0] == self.motion.namespace:
				cut_at = i+1
				# print('found', cut_at)
				break
		
		clist.CommandList.current += cmds.cut(0,-cut_at)
		self.r.end_speed(0)
		clist.CommandList.current += cmds.cut(-cut_at, None)
		# print('appending cmds', clist.CommandList.get().commands)
		
	def with_chain(self, end_speed=None):
		self.start()
		r = getattr(_e, self.motion.namespace)
		self.r = r
		@_e._do
		def later():
			nonlocal end_speed
			r.end_speed(end_speed)
		return self


class Motion:

	def __init__(self, name='Motion', packet_stream=None):
		self.name = name
		self.debug = 0
		self.point = [999999]*2
		self.tol = 0
		self.angle_sum = 0
		self.state_rep = 0
		self.ps = None
		self.future=None
		self.direction = 0
		self.disabled = False
		self.timeout = False
		self.wheel_distance = 282.5
		self.namespace = None
		self.cur_state = 'I'
		self.stuckpos_tol_dist = 80
		self.stuckpos_tol_orient = 15
		
		self.setting_position = 0
		self.setting_position_point = [0,0,0]
		
		self.cur_cmd = None
		self.cmd_verified = False
		self.cmd_verify_future = None
		
		from core.State import StateBase
		self._accel = StateBase(.250)
		self._speed = StateBase(0x25)
		self.wchain = WithChain(self)
		if packet_stream: self.set_packet_stream(packet_stream)
		
		
	def set_packet_stream(self, ps):
		self.ps = ps
		self.ps.recv = self.on_recv
		
	def print_cmd(self, name, *args):
		print(col.yellow, name+':', col.white, *args)
	
	def on_recv(self, pkt):
		
		if chr(pkt[0]) == 'L':
			pos = _core.get_position()
			_core.emit('motion:reset', pos)
			# print('sending l')
			self.send('l')
			
		if chr(pkt[0]) == 'P':
			
			if len(pkt) != 8: return
			s,x,y,a = chr(pkt[1]), l16(pkt, 2), l16(pkt, 4), l16(pkt, 6)
			_core.log('P', x,y,a, s, _type='motion')
			self.tol = 0
			norm_angle = normalize_orient(a-_core.get_orientation())
			if abs(norm_angle) < 10:
				self.angle_sum += norm_angle
			# print('angle_sum', self.angle_sum)
			# print(_core.look_vector())
			if self.tol > 0 and point_distance([x,y], self.point) < self.tol:
				self.resolve(True)
			
			prev = _core.state['state']
			if prev != s:
				self.state_rep = 0
			else:
				self.state_rep += 1
				
			if self.state_rep >= 5 and self.cur_state != s:
				ps = self.cur_state
				_core.log('state repeat issue', 'prev', ps, 'now', s, _type='motion')
				self.cur_state = s
				self.state_rep = 0
				
				if s == 'S':
					_core.emit('motion:stuck')
				if ps in 'MR' and prev == 'I':
					_core.emit('motion:glitch_blocked')
					# self.resolve(True)
					# print('glitch resolved')
			
			
			pos = _core.get_position()
			
			_core.state['state'] = s

			if self.setting_position == 1:
				_core.log('pt dist', self.setting_position, 
					point_distance([x,y], self.setting_position_point[:2]),
					abs(self.setting_position_point[2] - a), _type='motion')
				_core.log('pos:', pos, self.setting_position_point, _type='motion')
				
			if self.setting_position == 0 or \
				(self.setting_position == 1 and point_distance([x,y], self.setting_position_point[:2]) < 50 and
				abs(self.setting_position_point[2] - a) < 30):
					self.setting_position = 0
					_core.set_position(x,y,a)
			
		elif chr(pkt[0]) == 'p':
			
			status,x,y,a = chr(pkt[1]), l16(pkt, 2), l16(pkt, 4), l16(pkt, 6)
			
			# print('motion state:',status)
			prev = self.cur_state
			#print('ch state', x,y,a,status, 'prev:', prev)
			if self.cur_state == status: return
			self.cur_state = status
			# self.state_rep = 0
			if status == 'I':
				_core.emit('motion:idle')
				if prev in 'MR': self.resolve(True)
			elif status == 'S':
				_core.emit('motion:stuck')
			elif status == 'E':
				_core.emit('motion:error')
				# print('motion got error')
				pass
		elif chr(pkt[0]) == 'b':
			checksum = lu16(pkt, 1)
			if checksum != self.cur_cmd:
				return
				# print('wrong checksum', checksum, self.cur_cmd)
			else:
				# return
				_core.log('cmd hash is ok', _type='motion')
				if self.cmd_verify_future:
					self.cmd_verify_future.cancel()
				
		elif chr(pkt[0]) == 'C' and len(pkt) >= 6+1:
			# print(nice_hex(pkt))
			self.resolve( self.conf_bytes_to_float(pkt[1:]) )
		else:
			self.lift_recv(pkt)
			
	@_core.asyn2
	def tolerance(self,t):
		self.tol = t

	def resolve(self, v=True):
		if self.disabled: return
		if self.future:
			self.future.set_result(v)
			#print('resolved', id(self.future))
			self.future = None
			# self.cur_state = 'I'
			#print('motion resolved')
			# _core.notify(self.name)

	def check_hash(self):
		# return
		self.cmd_verify_future = None
		if not self.cmd_verified:
			# do repeat command
			# print('command is unverified')
			print('Motion board is not responding')
			if self.future:
				self.future.redo()
			
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
			# _core.log('cmd:', x, _type='motion')
			self.ps.send(x)
			
	
	def send2(self, x): # with verification
		if self.disabled: return
		_core.log('cmd:', x, _type='motion')
		self.cur_cmd = simple_hash(x)
		self.cmd_verified = False
		if self.cmd_verify_future:
			self.cmd_verify_future.cancel()
		# self.cmd_verify_future = _core.call_later(1, self.check_hash)
		self.send(x)
	
	@_core.asyn2
	def send_cmd(self, x):
		self.send(x)
	
		
	####### RAW COMMANDS #######
	def move_cmd(self, x,y,r=100,dir=1): self.send2(b'N' + p16(x) + p16(y) + p16(r) + p8(dir))
	def goto_cmd(self, x,y,dir=1): self.send2(b'G' + p16(x) + p16(y) + p8(dir))
	def absrot_cmd(self, a): self.send2(b'A' + p16(a))
	def curve_cmd(self, x,y,alpha,dir=1): self.send2(b'Q' + p16(x) + p16(y) + p16(alpha) + p8(dir))
	def turn_cmd(self, o): self.send2(b'T' + p16(o))
	def stop_cmd(self): self.send2(b'S')
	def motoroff_cmd(self): self.send(b's')
	def softstop_cmd(self): self.send(b't')
	def setpos_cmd(self, x=0,y=0,o=0): self.send2(b'I' + p16(x) + p16(y) + p16(o))
	def intr_cmd(self): self.send2(b'i')
	def forward_cmd(self, dist): self.send2(b'D' + p16(dist))
	def diff_drive_cmd(self, x,y,alpha,dir): self.send2(b'L' +  p16(x) + p16(y) + p16(alpha) + p8(dir))
	def motor_pwm_cmd(self, m1,m2): self.send(b'm' + p16(m1) + p16(m2))
	def const_speed_cmd(self, m1,m2): self.send(b'M' + p16(m1) + p16(m2))
	def curve_rel_cmd(self, r, alpha): self.send2(b'q' +  p16(r) + p16(alpha))
	def speed_cmd(self, s): self.send(b'V' + p8(s))
	def reset_cmd(self): self.send(b'R')
	#############################
	
	def on_cancel(self):
		print('motion cancel')
		if self.future:
			self.intr()
		self.future = None
		self.cancelling = True
		# self.softstop()
		# self.intr()
		# print('on cancel')
		# self.cur_state = 'I'
	
	@_core.asyn2
	def reset(self):
		self.reset_cmd()
			
	def export_cmds(self, namespace='r'):
		self.namespace = namespace
		with _core.export_ns(namespace):
			_core.export_cmd('goto', self.goto)
			_core.export_cmd('speed', self.speed)
			_core.export_cmd('curve', self.curve)
			_core.export_cmd('curve_rel', self.curve_rel)
			_core.export_cmd('diff_drive', self.diff_drive)
			_core.export_cmd('forward', self.forward)
			_core.export_cmd('absrot', self.absrot)
			_core.export_cmd('turn', self.turn)
			_core.export_cmd('relrot', self.turn) # alias
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
			_core.export_cmd('chain', self.wchain.with_chain)
			_core.export_cmd('reset', self.reset)
			
			_core.export_cmd('end_speed', self.end_speed)
			# lift mode
			_core.export_cmd('lift', self.lift)
			_core.export_cmd('prepare_lift', self.prepare_lift)
		
	def set_direction(self, d):
		_core.state['direction'] = d
		
	@_core.asyn2
	def speed(self, s, _sim):
		self._speed.val = s
		if not _sim:
			self.accel(self._accel.val*1000, _sim)
			self.speed_cmd(s)
	
	@_core.asyn2
	def end_speed(self, speed=None, _sim=0):
		if speed == None:
			speed = self._speed.val
		self._end_speed = speed
		print('end speed', speed)
		if not _sim:
			self.conf_set('end_speed', speed)
	
	def accel(self, a=None, _future=None, _sim=None):
		if a: self._accel.val = a/1000
		ret = self._accel.val * 1000
		if _future:
			_future.set_result(ret)
		else:
			return ret
		if a and not _sim:
			self.conf_set('accel', a, _sim)
			self.conf_set('alpha', a, _sim)
	
	@_core.module_cmd
	def diff_drive(self,x,y,alpha, dir=1):
		# TODO: add sim iface
		self.print_cmd('diff drive',x,y,alpha)
		self.diff_drive_cmd(x,y,alpha, dir)
	
	@_core.module_cmd
	def forward(self, dist, _sim=0, _pause=0):
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
			
		self.set_direction( 1 if dist > 0 else -1 )
		if _pause == 2:
			dist = int(dist - math.copysign(_core.distance_to( self.old_pt ), dist))
			self.print_cmd('resume forward', dist)
		elif _pause == 1:
			self.print_cmd('pause forward')
			return
		elif _pause == 4:
			self.print_cmd('cancel forward')
			return
		elif _pause == 0:
			self.old_pt = _core.get_point()
			self.print_cmd('forward', dist)
		self.forward_cmd(dist)
	
	@_core.asyn2
	def intr(self):
		self.intr_cmd()
		
	def fullstop(self):
		self.intr_cmd()
		self.motoroff_cmd()
		self.disabled = True
		
	@_core.module_cmd
	def move(self, x,y,r=100,o=1):
		self.print_cmd('moving to',x,y,o)
		x,y=int(x),int(y)
		self.point = [x,y]
		# self.intr()
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
	
	@_core.module_cmd
	def softstop(self):
		if _core.cur_state == 'I':
			self.future.set(0)
		else:
			self.print_cmd('softstop')
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
		#print('absrot', id(self.future))
		self.absrot_cmd(a)
	
	@_core.module_cmd
	def curve(self, x,y,alpha,dir=1, _sim=0, _pause=0):
		if _sim:
			r = int( _core.distance_to([x,y]) )
			t = 0
			if r > 0: 
				s = 1 if alpha > 0 else -1
				dir = 1 if dir > 0 else -1
				t=self.absrot( int( vector_orient( _core.vector_to([x,y]) ) + dir * -s * 90 ), _sim=1 )
			return self.curve_rel( r, alpha, _sim=1 ) + t
		
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
		
		if _pause == 2:
			alpha = int((self.old_orient + alpha) - self.angle_sum)
			self.print_cmd('resume curve', x, y, alpha, dir)
		elif _pause == 1 or _pause == 4:
			self.print_cmd('pause curve')
			return
		elif _pause == 0:
			
			s = 1 if alpha > 0 else -1
			dir = 1 if dir > 0 else -1
			rot=int( vector_orient( _core.vector_to([x,y]) ) + dir * -s * 90 )
			self.set_direction(math.copysign(1,dir))
			self.old_orient = self.angle_sum + rot
			self.print_cmd('curve',x,y,alpha,dir)
		# self.print_cmd('curve',x,y,alpha,dir)
		self.curve_cmd(x,y, alpha, dir)
	
	@_core.module_cmd
	def curve_rel(self, r, angle, dir=1, _sim=0, _pause=0):
		
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
			
			L_dist = abs(L_dist)
			T1 = T3 = speed / accel;
			L1 = accel * T1 * T1 / 2;
			
			if L1 > L_dist / 2:
				L1 = L_dist / 2;
				T1 = T3 = math.sqrt(2 * L1 / accel);
				T2 = 0;
			else:
				T2 = (L_dist - 2*L1) / speed;
			return T1+T2+T3
		self.set_direction(math.copysign(1,angle))
		if _pause == 2:
			angle = int( math.copysign(1,r) * ((self.old_orient + math.copysign(1,r)*angle) - self.angle_sum))
			self.print_cmd('resume curve rel', r, angle)
		elif _pause == 1:
			self.print_cmd('pause rel', r, angle)
			return
		elif _pause == 4:
			self.print_cmd('cancel rel', r, angle)
			return
		elif _pause == 0:
			self.old_orient = self.angle_sum
			# print('curve_rel oldorient',self.old_orient)
			self.print_cmd('curve rel', r, angle)
		
		self.curve_rel_cmd(r, angle)
	
	@_core.module_cmd
	def turn(self, o, _sim=0, _pause=0):
		
		if _sim:
			if o == 0: return 0
			# Fi is not really angle here, but distance to travel, as circumference
			Fi_abs = abs(math.radians(o) * self.wheel_distance/2)
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
		
		if _pause == 2:
			o = int((self.old_orient + o) - self.angle_sum)
			self.print_cmd('resume turn', o)
		elif _pause == 1:
			self.print_cmd('pause forward')
			return
		elif _pause == 0:
			self.old_orient = self.angle_sum
			self.print_cmd('turn', o)
			
		if o == 0: 
			self.resolve()
			return

		self.turn_cmd(o)
	
	@_core.asyn2
	def stop(self):
		self.print_cmd('stop')
		self.stop_cmd()
	
	
	def modpos(self, x=None,y=None,o=None):
		new=[x,y,o]
		p = list(_core.get_position())
		for i in range(3):
			if new[i] != None: p[i] = int(new[i])
		return p
	
	@_core.asyn2
	def setpos(self, x=None,y=None,o=None,_sim=0):
		p = self.modpos(x,y,o)
		self.setting_position = 1
		self.setting_position_point = p
		# print('setpos modpos', x,y,o)
		_core.set_position(*p)
		if not _sim:
			self.print_cmd('setpos', *p)
			self.setpos_cmd(*p)
		
		
	
	def stuckpos(self, forw=1, x=None,y=None,o=None,check=False, _sim=0):
		m = getattr(_e, self.namespace)
		@_e._do
		def _():
			p=m.conf_set('enable_stuck', 1)
			@_e._on('motion:stuck')
			def on_stuck():
				print('handling stuck')
				_e._goto('stuckpos_label', ref=p)
			m.forward(forw * 500)
			_e._L('stuckpos_label')
		
		# test if we hit some obstacle
		# our new position and real position shouldn't change much
	
		if not check:
			f = Future()
			m.setpos(x,y,o)
			f.set(True)
			return f
		
		def check_pos():
			p = self.modpos(x,y,o)
			cpos = _core.get_position()
			diff_dist = point_distance(p[:2], cpos[:2])
			diff_orient = normalize_orient(p[2] - cpos[2])
			print(diff_dist, diff_orient)
			if abs(diff_dist) < self.stuckpos_tol_dist and abs(diff_orient) < self.stuckpos_tol_orient:
				m.setpos(x=x, y=y, o=o)
				return True
			else:
				_core.emit('motion:stuckposfail')
				return False
		
		return _e._do(check_pos)
	
	def run(self):
		self.cur_state = 'I'
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
	def conf_set(self, k, v, dec=4, _sim=0):
		if k == 'wheel_distance':
			self.wheel_distance = v
		elif k in ('accel','alpha'):
			self.accel(v, _sim=1)
		
		if _sim:
			return

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

	
	

	
	################# Linear Mode ##############
	lift_fut=[None,None]
	lift_positions=[{},{}]
	
	def lift_recv(self, p):
		if p[0] == 0x40:
			if self.lift_fut[1]:
				self.lift_fut[1].set_result(1)
		elif p[0] == 0x21:
			if self.lift_fut[0]:
				self.lift_fut[0].set_result(1)

	
	def prepare_lift(self, _future):
		self.future = _future
		if State.sim: _future.set_result(1)
		self.send('/')

	def set_lift_positions(self, l, positions):
		self.lift_positions[l-1] = positions
		
	def lift(self, l, pos, up=0, _future=None):
		if State.sim: _future.set_result(1)
		l = min(2, max(1, l))
		if not self.lift_fut[l-1]: 
			self.conf_set('encoder'+str(l)+'_max', 2000000)
		p = self.lift_fut[l-1]
		if p and not p.done(): print('lift unfinished !')
		self.lift_fut[l-1] = _future
		pt = 0
		lf = self.lift_positions[l-1]
		if pos in lf:
			pt = lf[pos]
		elif type(pos) is int:
			pt = pos
		self.conf_set('setpoint'+str(l), pt - 200000 * up)
			
