import time
from core.Util import col

@_core.export_cmd
def an_func(a, _future, _pause=None):
	# _future.val=1
	print('an_func', a, _future, ': pause:', _pause)
	
	def on_cancel():
		print('an_func, on_cancel called')
		
	
	def f():
		_future.val=1
		print('future done')
	
	if _pause == 1:
		_future.passed = time.time()
		_future.st.cancel()
		print('an_func pausing')
		
	elif _pause == 2:
		_future.st = _core.call_later(5 - (_future.passed - _future.time), f)
		print('an_func resuming')
	elif _pause == 4:
		print('cancel pause = 4')
	else:
		_future.set_on_cancel(on_cancel)
		_future.time = time.time()
		_future.st = _core.call_later(5, f)

def run():
	
	@_spawn
	def _():
		sleep(2)
		_sync(1, ref='main')
		sleep(2)
		_wake('main')
	
	an_func(10)

	####################################
	_print(col.yellow, 'test case cancellation', col.white)
	
	@_spawn
	def _():
		sleep(2)
		_sync(1, ref='main')
		sleep(2)
		# main jumps to here
		_goto('here', ref='main')
		# _wake('main')

	an_func(10)
	
	_L('here')
	
	######################################
	
