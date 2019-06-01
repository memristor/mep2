State.goldenium_activated = _State(0)
State.goldenium_picked = _State(0)
def run():
	r.conf_set('send_status_interval', 10)
	State.color = 'ljubicasta'
	State.startpos = (-1195, -610)
	r.setpos(-1500+175+138,-610,90) # red
	napgold(0)
	nazgold(0)
	rrucica(0)
	lrucica(0)
	rfliper(0)
	lfliper(0)
	r.speed(50)
	
	
