def run():
	
	@_spawn
	def _():
		_print('thread1 sleeping')
		sleep(0.5)
		
		_print('thread1 crossing label1')
		
		# entering(consuming) label1
		_L('label1')
	
	_print('main thread waiting for thread1 to cross label1')
	
	# waiting for label1
	_sync('label1')
	
	_print('main thread continuing')
