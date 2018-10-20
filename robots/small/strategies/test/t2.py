weight=9
def leave():
	print('leaving task t2')
	sleep(5)
	_do(lambda: print('after sleep'))
	sleep(5)
	
def run():
	
	print('t2')
	_do(lambda: print('hehe'))
	#  _task_suspend()
	def test():
		_label('hehe')
	s=_spawn(test)
	def lol():
		_label('haha')
		#  sleep(2)
		_task_suspend()
		_label('yay')
	s1=_spawn(lol)
	sleep(2)
	#  _sync(s1)
	_do(lambda: print('lol'))
	#  return False
	#  sleep(10)
