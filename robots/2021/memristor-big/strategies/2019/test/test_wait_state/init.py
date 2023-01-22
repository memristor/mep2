a = _State(0, 'a', shared=1)
def run():
	@_spawn
	def _():
		sleep(5)
		_sync(1, ref='main')
		_print('pausing main')
		sleep(0.5)
		_print('continuing main')
		_wake('main')
		_sync(1, ref='main')
		_print('pausing main')
		sleep(0.5)
		_print('continuing main')
		_wake('main')
		_sync(1, ref='main')
		_print('pausing main')
		sleep(0.5)
		_print('continuing main')
		_wake('main')
	_print('wait for a')
	with _while(lambda: a.val == 0): pass
	
	_print('hehe')
