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
		sleep(0.5)
		_goto('lbl')
		_print('end')

	sleep(5)
	_emit('hehe')
	sleep(5)
	_emit('hehe')
	sleep(5)
	_emit('hehe')
	sleep(5)
