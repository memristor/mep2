def run():

#with _while(1):
#with _e._parallel():

	with _parallel():
		rfliper(2)
		lfliper(2)
	_sync()


	with _parallel():
		rfliper(1)
		lfliper(1)
	_sync()
	
	sleep(0.1)
	with _parallel():
		llift(0)
		rlift(0)
	_sync()
	sleep(0.1)

	pump(0, 1)

	sleep(0.3)
	with _parallel():
		rlift(1)
		llift(1)
	_sync()
	sleep(1)

	with _parallel():
		rfliper(2)
		lfliper(2)
	_sync()



	with _parallel():
		rfliper(1)
		lfliper(1)
	_sync()


	with _parallel():
		rfliper(2)
		lfliper(2)
	_sync()


	sleep(1)
	with _parallel():
		llift(0)
		rlift(0)
	_sync()
	sleep(0.1)


	sleep(0.2)


	with _parallel():
		rfliper(1)
		lfliper(1)
	_sync()

	sleep(1)
	
	with _parallel():
		rlift(1,.1)
		llift(1,.1)
	_sync()

	@_spawn
	def _():
		for i in range(5):
			pump(0, 0)
			sleep(.2)	

	pump(0, 0)
	sleep(0.5)
	with _parallel():
		rlift(1)
		llift(1)
	_sync()


	with _parallel():
		rfliper(2)
		lfliper(2)
	_sync()





