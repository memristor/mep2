weight=1
a=_State(0)
def run():
	_print('exec task')

	if a.val <= 5:
		_task_suspend()

def leave():
	_print('leaving', a.val)
	a.inc()
	sleep(1)
	if a.val <= 4:
		_task_suspend()
