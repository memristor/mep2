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
class Servo:
	def __init__(self, name, servo_id, packet_stream=None):
		self.name = name
		self.servo_id = servo_id
		self.ps = packet_stream
		
	def set_packet_stream(self,ps):
		self.ps = ps
	
	def action(self, f, val=None):
			
		if f not in servo_commands:        
			print('function ' + f + ' doesn\'t exist')
			return

		servo_id = self.servo_id
		
		cmd = servo_commands[f]
		servo_len = 4
		servo_func = cmd[0]
		servo_rw = cmd[1]
		servo_fmt = cmd[2]

		if val == None and 'R' not in servo_rw:
			print('function ' + f + ' is not readable')
			return

		if val != None and 'W' not in servo_rw:
			print('function ' + f + ' is not writable')
			return

		if val == None:
			servo_rw = 2
			servo_fmt = ''
		else:
			servo_rw = 3

		if val == None:
			servo_len = 3
		elif servo_fmt == 'h':
			servo_len += 1

		#  if addr == None:
			#  addr = 0x7f00 if type(which) is int or servo[0] == 'ax' else 0x7f01
		fmt = '4B'+servo_fmt
		data = [servo_id, servo_len, servo_rw, servo_func]
		if val != None:
			data += [val]

		self.ps.send(struct.pack(fmt, *data))
		#  if val == None:
			#  print('Sent request, waiting for answer')
			#  while True:
				#  frame = self._dissect_can_frame(self.s.recv(16))
				
				#  if frame[0] == (addr | self.use_eff) and frame[1] > 0:
					#  print(hex(frame[0]), Can.nice_hex(frame[2]))
					#  return
						
	def listServoCmds():
		print('Servo commands:')
		for i in sorted(servo_commands):
			print('\t' + i)

	def listServo():
		print('Servo list:')
		for i in sorted(robot_servos):
			print('\t' + i)

	def listActuators():
		print('Actuators, Sensors:')
		for i in sorted(robot_byte_act):
			print('\t' + i)
