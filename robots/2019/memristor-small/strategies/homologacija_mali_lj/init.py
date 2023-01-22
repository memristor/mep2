
State.PS_veliki=_State(False,name='PS_veliki',shared=True)
State.PS_mali=_State(False,name='PS_mali',shared=True)
def run():
	r.conf_set('send_status_interval', 10)

	r.setpos(-1500+308,-1000+390,90)
	r.speed(120)
	nazgold(0)
	napgold(0)
	lfliper(0)
	rfliper(0)
	rrucica(0)
	lrucica(0)
