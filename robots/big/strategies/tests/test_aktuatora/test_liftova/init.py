def run():

#with _while(1):
#with _e._parallel():
	
	llift(1)
	rlift(1)
	_sync()

	with _parallel():
		llift(0)
		rlift(0)
	_sync()



	with _parallel():
		llift(1)
		rlift(1)
	_sync()
