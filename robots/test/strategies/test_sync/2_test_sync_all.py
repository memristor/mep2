order=2
a=_State(1)
def run():
	_print('test case1')
	a.val = 0
	@_spawn
	def _():
		_print('sleep1')
		sleep(5)
		a.val = 5
		
		@_spawn
		def _():
			sleep(2)
			_print('sleep1_1 done')
		@_spawn
		def _():
			sleep(1)
			_print('sleep1_2 done')
		_sync()
		_print('speed1 done')
		
	@_spawn
	def _():
		_print('sleep2')
		sleep(2)
		a.val = 5
		_print('sleep2 done')
	
	_sync()
	
	@_do
	def _():
		if a.val != 5:
			print('fail')
			bad()


	_print('test case2')
	
	@_spawn
	def _():
		sleep(5)
		_emit('hehe')
	_sync(evt='hehe')

	# _redo()
