
def run():
	_print('\ttest 1')
	
	lift(1, 'accel')
	_print('\tlift 1 done')
	lift(2, 'accel')
	_print('\tlift 2 done')


	lift(1, 'pri_vrhu')
	lift(2, 'pri_vrhu')
	
	_print('\tpri vrhu done')

	with _parallel():
		lift(1, 'accel')
		lift(2, 'accel')

	_sync()

	_print('\tsync accel done')

	with _parallel():
		lift(1, 'pri_vrhu')
		lift(2, 'pri_vrhu')

	_sync()

	_print('\tpri vrhu done')
