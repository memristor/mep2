weight=3
def run():
	_print('2')
	sleep(4)
	_task_suspend('t1')
	
	_print('shouldnt gethere')
