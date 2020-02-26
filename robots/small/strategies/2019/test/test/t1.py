weight=1
def run():

	@_spawn
	def _():
		_print('test')
		_label('a')	
		sleep(1)
		_emit('msg')
		_goto('a')

	@_spawn(_name='pauser')
	def _():
		sleep(4)
		_sync(ref='thread')

	@_spawn(_name='redoer')
	def _():
		sleep(6)
		_redo(ref='thread')

	@_spawn(_name='thread')
	def _():

		@_do(_atomic=1)
		def _():

			@_listen('msg')
			def _():
				print('got msg')
			_label('t')
			sleep(1)
			_print('doing thread')
			sleep(1)
			_print('doing thread')
			_goto('t')

	sleep(20)
