def run():

#with _while(1):
#with _e._parallel():

	with _parallel():
		rfliper(2)
		lfliper(2)
	_sync()

	r.forward(200)

	with _parallel():
		rfliper(1)
		lfliper(1)
	_sync()
	
	with _parallel():
		llift(0)
		rlift(0)
	_sync()

	pump(0, 1)

	with _parallel():
		rlift(1)
		llift(1)
	_sync()

	with _parallel():
		rfliper(2)
		lfliper(2)
	_sync()

	r.forward(200)


	with _parallel():
		rfliper(1)
		lfliper(1)
	_sync()

	r.forward(-200)

	with _parallel():
		rfliper(2)
		lfliper(2)
	_sync()

	r.forward(-200)

	with _parallel():
		llift(0)
		rlift(0)
	_sync()

	pump(0, 0)

	sleep(2)

	with _parallel():
		rfliper(1)
		lfliper(1)
	_sync()

	with _parallel():
		rlift(1)
		llift(1)
	_sync()

	r.forward(-100)


	with _parallel():
		rfliper(2)
		lfliper(2)
	_sync()





