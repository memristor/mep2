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
		lok_visina(1023)
		rok_visina(1023)
	_sync()

	pump(0, 1)

	with _parallel():
		rok_visina(-1023)
		lok_visina(-1023)
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
		lok_visina(1023)
		rok_visina(1023)
	_sync()

	pump(0, 0)

	sleep(2)

	with _parallel():
		rfliper(1)
		lfliper(1)
	_sync()

	with _parallel():
		rok_visina(-1023)
		lok_visina(-1023)
	_sync()

	r.forward(-100)


	with _parallel():
		rfliper(2)
		lfliper(2)
	_sync()





