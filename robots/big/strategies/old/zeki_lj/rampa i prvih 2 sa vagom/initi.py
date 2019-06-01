weight = 50
def run():
	r.setpos(-1280,-250,0) #ljubicasta
	#r.setpos(-1435,345,180) #testiranje paralelno sa plavom
	r.conf_set('send_status_interval', 10)
	# init servos
	llift(0)
	rlift(0)
	rfliper(0)
	lfliper(0)
	

	
	return