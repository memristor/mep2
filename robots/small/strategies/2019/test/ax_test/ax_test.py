weight=4
def run():
	# with _while(1):
	
	with _while(1):
		with _parallel():
			rrucica(1)
			lrucica(1)
		_sync()
		sleep(1)
		with _parallel():
			rrucica(0)
			lrucica(0)
		_sync()
		sleep(1)
	return
	sleep(5)
	rrucica(0)
	lrucica(0)
	sleep(5)
	
		
	with disabled("collision"):
		rfliper(2)
		lfliper(2)
		sleep(5)
		lfliper(1)
		rfliper(1)
		sleep(2)
		lfliper(0)
		rfliper(0)
		
		#nazgold(1)
		'''
		sleep(2)
		nazgold(2)
		sleep(2)
		nazgold(1)
		sleep(2)
		nazgold(0)
		sleep(80)'''
	# nazgold(1)
	# nazgold(2)
	# sleep(2)
	# nazgold(1)
	# return
	#napgold(2)
	# r.forward(100)
	#sleep(3)
	# pump(2,1)
	# pump(1,1)
	# sleep(3)
	# r.forward(-100)
	#napgold(0)
	#sleep(3)
	# return
	#napgold(1)
	# sleep(2)
	# return
	# sleep(2)
	# napgold(1)
	# sleep(2)
	# napgold(0)
	# return
	# sleep(3)
	# return
	#rfliper(2)
	#	lfliper(2)
	#sleep(80)
	'''lfliper(0)
	rfliper(0)
	sleep(2)
	lfliper(1)
	rfliper(1)
	sleep(2)
	lfliper(2)
	rfliper(2)
	sleep(2)
	lfliper(1)
	rfliper(1)
	sleep(2)
	lfliper(0)
	rfliper(0)'''
	

	'''rrucica(1)
	sleep(2)
	rrucica(0)
	lrucica(1)
	sleep(2)
	lrucica(0)'''
	
	#napgold(1)
	#napgold(0)
	'''	
	nazgold(0)
	sleep(2)
	nazgold(1)
	sleep(2)
	nazgold(2)
	sleep(2)
	nazgold(3)
	sleep(2)	
	nazgold(2)
	sleep(2)
	nazgold(1)
	sleep(2)
	nazgold(0)
	'''
	
			
