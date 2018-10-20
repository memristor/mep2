	def actuator(self, which, val=None):
		'''
			which - which actuator to send data to
			val - value to write
				(omitt if reading sensor)
		'''
		
		if type(which) is int:
			self.raw(which, 'B', [val])
		else:
			if which not in robot_byte_act:
				print('sensor or actuator ' + which + ' doesn\'t exist')
				return

			act = robot_byte_act[which]

			if val != None and 'W' not in act[1]:
				print('Cannot write to sensor')
			
			if val == None and 'R' not in act[1]:
				print('Cannot read from actuator')

			data = []
			if val != None:
				data = [val]
			else:
				print("reading from sensor not implemented yet")
				#self.raw(act[0], 'B', [val])

			self.raw(act[0], 'B', [val])
