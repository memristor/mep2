#weight = 50
State.PS_veliki=_State(False,name='PS_veliki',shared=True)
State.PS_mali=_State(False,name='PS_mali',shared=True)
def run():
	r.setpos(-1500+155+125+10,-1000+600+220,90) #bocno absrot90
	r.conf_set('send_status_interval', 10)
	State.color = 'ljubicasta'
	# init servos
	llift(0)
	rlift(0)
	rfliper(0)
	lfliper(0)
	return
