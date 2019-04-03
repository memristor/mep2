def run():
	r.conf_set('send_status_interval', 10)

	State.startpos = (1195, -610)
	r.setpos(1195,-610,90) # red
	napgold(0)
	nazgold(1)
	rrucica(0)
	lrucica(0)
	r.speed(140)
	
