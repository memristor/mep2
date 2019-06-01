weight=1
def run():
	_print('enter task')
	def _():
		print('lol2')
		_print('lol')

	a=_listen('lol', _)
	_emit('lol')
	_unlisten(a)
	_print('aft unl')
	_emit('lol')
	
	_print('aft lsn')
	_listen(a)
	_emit('lol')
	
	with disabled(a):
		_print('w disabled')
		_emit('lol')
	
	sleep(1)
	_task_suspend()
	
def leave():
	_print('on leave')
	_emit('lol')
	sleep(1)
