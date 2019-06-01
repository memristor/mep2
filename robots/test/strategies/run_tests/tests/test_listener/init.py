a=_State(0)
def run():
	
	@_listen('hehe')
	def _():
		_repeat('duplicate')
		a.val = 0
		_label('lbl')
		_print('start')
		a.inc()
		@_do
		def _():
			print('a.val: ', a.val)
		sleep(0.01)
		_goto('lbl')
		_print('end')

	sleep(0.1)
	_emit('hehe')
	sleep(0.1)
	_emit('hehe')
	sleep(0.1)
	_emit('hehe')
	sleep(0.1)
