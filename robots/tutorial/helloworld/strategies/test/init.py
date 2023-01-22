def run():
	
	@_spawn
	def t():
		_print('spawned')
		_goto(1, ref='main')
	sleep(10)
	_print('skipped')
	sleep(10)
	_print('done')
