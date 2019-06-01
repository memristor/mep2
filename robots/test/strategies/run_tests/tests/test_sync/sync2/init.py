def run():
	_print('tcase 1')
	with _parallel():
		sleep(3)
		sleep(2)
		
	_sync()
	
	_print('tcase 2')
	with _parallel():
		sleep(3)
		sleep(2)
		
	_sync()
