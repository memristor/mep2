weight=1
def run():
	_print('test1')
	
	_L('start')
	_print('starting')
	@_spawn
	def _():
		_print('goting')
		sleep(1)
		# _goto(offset=0, ref='main') # repeat sleep
		# _goto(offset=1, ref='main') # skip sleep
		# _goto(offset=10, ref='main') # overjump => task done
		# _goto(offset=-999, ref='main') # restart task
		_goto('start', ref='main') # restart task
		_print('goting 2')
	sleep(5)
	_print('done')
