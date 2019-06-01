
weight= 4
def run():
	r.speed(100)
	for i in range (5):
		_print(' absrot 0 ')

		r.absrot(0)
		sleep(2)


		_print(' absrot 10 ')

		r.absrot(10)
		sleep(2)
		
		_print(' absrot 0 ')

		r.absrot(0)
		sleep(2)
		
		_print(' absrot -10 ')

		r.absrot(-10)
		sleep(2)
		
		
		
		_print(' ab0srot 110 ')

		r.absrot(110)
		sleep(2)
		
		
		
		_print(' ab0srot *110 ')

		r.absrot(-110)
		sleep(2)		
	return
	
