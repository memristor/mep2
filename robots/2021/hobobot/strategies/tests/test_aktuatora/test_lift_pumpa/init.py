def run():

#with _while(1):
#with _e._parallel():


	with _parallel():
		llift(0)
		rlift(0)
	_sync()
	sleep(10)

	pump(0, 1)
	
	sleep(1)

	pump(0, 1)
