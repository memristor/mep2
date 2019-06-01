def run():
	
	_print('tof test')

	@_core.do
	def read_tof(idx):
		a = tof.measure(idx)
		@_do
		def _():
			print('TOF',idx,' got: ', a.val)
			
	# for i in range(8):
		# sleep(0.1)
		# _print('shuttin', i)
		# tof.start(i)
		# tof.stop(i)
	# sleep(5)
	# with _while(lambda: b.val < 10):
	
	# z = tof.measure(7)
	# @_do
	# def _():
		# r.forward(150 + 20 - z.val)
	# return
	
	
	# for j in range(8):
		# for i in range(120):
			# read_tof(j)
		# tof.stop()
	
		# b.inc()
	# s1 = 6
	# s2 = 4
	s1 = 7
	s2 = 3
	tof.start(s1)
	tof.start(s2)
	State.val = 0
	
	# @_spawn
	# def _():
		# with _while(1):
			# sleep(0.5)
			# @_do
			# def _():
				# r.turn(int(State.val))
			
	# with _while(1):
	@_core.do
	def align():
		a=tof.measure(s1)
		b=tof.measure(s2)
		@_do
		def _():
			import math
			
			# val = math.degrees(math.atan2(a.val-(116-92)-b.val, 115))
			val = math.degrees(math.atan2(a.val-(56-82)-b.val, 200))
			State.val = val
			print(a.val, b.val, State.val)
			
			r.turn(int(val))
	align()
	
	# @_core.do
	# def get_closer(dist):
		
	
