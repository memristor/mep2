def run():

#with _while(1):
#with _e._parallel():
	
	lok_visina(1023)
	rok_visina(1023)
	_sync()

	with _parallel():
		rok_visina(-1023)
		lok_visina(-1023)
	_sync()
