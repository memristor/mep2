
def run():
	r.setpos(1500-155-125,-1000+600+220,90) #bocno absrot90
	r.conf_set('send_status_interval', 10)
	r.speed(100)
	State.color = 'zuta'
	# init servos
	llift(0)
	rlift(0)
	rfliper(0)
	lfliper(0)
	return