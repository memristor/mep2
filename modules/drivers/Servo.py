servo_commands = {
	'ModelNumber': [0, 'R', 'h'],

	'SetId': [3, 'RW', 'B'],
	'SetBaud': [4, 'RW', 'B'],
	'ReturnDelayTime': [5, 'RW', 'B'],
	'CWAngleLimit': [6, 'RW', 'h'],
	'CCWAngleLimit': [8, 'RW', 'h'],
	'HLimitTemp': [11, 'RW', 'B'],
	'MinVoltage': [12, 'RW', 'B'],
	'MaxVoltage': [13, 'RW', 'B'],
	'MaxTorque': [14, 'RW', 'h'],
	'Status': [16, 'RW', 'B'],
	'AlarmLED': [17, 'RW', 'B'],
	'AlarmShutdown': [18, 'RW', 'B'],
	'TorqueEnable': [24, 'RW', 'B'],
	'LED': [25, 'RW', 'B'],
	'CWComplianceMargin': [26, 'RW', 'B'],
	'CCWComplianceMargin': [27, 'RW', 'B'],
	'CWComplianceScope': [28, 'RW', 'B'],
	'CCWComplianceScope': [29, 'RW', 'B'],
	'GoalPosition': [30, 'RW', 'h'],
	'Speed': [32, 'RW', 'h'],
	'TorqueLimit': [34, 'RW', 'B'],
	'PresentPosition': [36, 'R', 'h'],
	'PresentSpeed': [38, 'R', 'h'],
	'PresentLoad': [40, 'R', 'h'],
	'PresentVoltage': [42, 'R', 'B'],
	'PresentTemp': [43, 'R', 'B'],
	'Punch': [48, 'RW', 'h'],
}
import struct
from core.Convert import l16
class Servo:
	def __init__(self, name, servo_id, packet_stream=None):
		self.name = name
		self.servo_id = servo_id
		self.ps = packet_stream
		self.prev_val = 0
		self.servo_tries = 0
		self.cur_action = None
		self.future = None
		self.wheel_mode = False
		
	def set_packet_stream(self,ps):
		self.ps = ps
		
	def export_cmds(self, ns=''):
		with _core.export_ns(ns):
			_core.export_cmd('action', self.action)
			_core.export_cmd('wheelspeed', self.wheelspeed)
		self.namespace = ns

	@_core.module_cmd
	def action(self, f, val=None, poll=True, _sim=0):
		if f not in servo_commands:
			print('function ' + f + ' doesn\'t exist')
			return

		if _sim:
			self.future.set(1)
			return
		servo_id = self.servo_id
		print('servo', self.name, 'action', f, val)
		cmd = servo_commands[f]
		servo_len = 4
		servo_func = cmd[0]
		servo_rw = cmd[1]
		pfmt=servo_fmt = cmd[2]

		if val == None and 'R' not in servo_rw:
			print('function ' + f + ' is not readable')
			return

		if val != None and 'W' not in servo_rw:
			print('function ' + f + ' is not writable')
			return

		if val == None:
			servo_rw = 2
			servo_fmt = 'B'
			servo_len = 4
		else:
			servo_rw = 3
			if servo_fmt == 'h':
				servo_len += 1

		#  if addr == None:
			#  addr = 0x7f00 if type(which) is int or servo[0] == 'ax' else 0x7f01
		fmt = '4B'+servo_fmt
		data = [servo_id, servo_len, servo_rw, servo_func]
		if val != None:
			data += [val]
			self.val = val
		else:
			data += [2] if pfmt == 'h' else [1]
			
		self.ps.send(struct.pack(fmt, *data))
		# print('data send', data)
		
		if (State.sim and self.future) or (self.future and State.get('ignore_servo')):
			self.future.set_result(1)
		else:
			# print(self.servo_id, self.name, 'starting cmd', f, self.val)
			self.cur_action = f
			if poll and f == 'GoalPosition' and self.val != None:
				self.poll_status()
				
			elif f not in ('GoalPosition', 'PresentPosition') and self.future:
				self.future.set_result(1)
		
		
	def poll_status(self):
		self.action('PresentPosition', None, poll=False)
		if self.val != None:
			_core.loop.call_later(0.1, self.poll_status)
		
		
	def recv(self, data):
		if self.cur_action != 'PresentPosition' or not self.val or len(data) < 5:
			return
		# print(self.servo_id, self.cur_action, data)
			
		if data[0] != self.servo_id:
			return
		
		if len(data) >= 5:
			# print(self.servo_id, 'unpaking: ' , data, self.val)
			r = struct.unpack('h', data[3:])[0]
			# print('servo',data, r)
			if abs(r - self.prev_val) < 50:
				self.servo_tries += 1
			else:
				self.servo_tries = 0
				
				
			if self.servo_tries > 10:
				if self.future: self.future.set(0)
				self.val = None
			self.prev_val = r
			print('servo', self.name, self.servo_tries)
			
			if self.val != None and abs(r - self.val) < 50:
				if self.future: self.future.set(1)
				self.val = None
				print('servo', self.name, 'finished')

	@_core.do
	def wheelspeed(self, speed):
		ns = getattr(_e, self.namespace)
		if not self.wheel_mode:
			ns.action('CCWAngleLimit', 0)
			ns.action('CWAngleLimit', 0)
			self.wheel_mode = True
		ns.action('Speed', speed if speed >= 0 else -speed+1024)
	
	def run(self):
		# print('runnin')
		self.ps.recv = self.recv
