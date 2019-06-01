order=2
a=_State(1)
def run():
	_print('test case1')
	a.val = 0
	_print('ok')
	
	@_spawn
	def _():
		# sleep(0.1)
		_sync(1,ref='main')
		sleep(.2)
		_print('continuing')
		_wake('main')
	
	# sleep(0.05)
	@_do
	def _():
		# _print('th1')
		sleep(.1)
		_print('doing1')
		_print('hehe')
	
	@_spawn
	def _():
		_print('sleep1')
		# return
		sleep(.5)
		a.val = 5
		
		@_spawn
		def s():
			sleep(.2)
			_print('sleep1_1 done')
		@_spawn
		def s():
			sleep(.1)
			_print('sleep1_2 done')
		_sync()
		_print('speed1 done')
		
	
	_print('syncing')
	_sync()
	_print('done')
