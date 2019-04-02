weight=1
a=_State(name='an var', shared=True)
def run():
	
	@_spawn
	def _():
		
		@_listen('an_event')
		def _():
			_print('an_event')
			bad()
		
		@_spawn
		def _():
			sleep(5)
			_print('sleep1_1 done')
			bad()
			

		sleep(3)
		_print('sleep1 done')
		
	sleep(0.1)
	sleep(4)
	_emit('an_event')
	sleep(6)
