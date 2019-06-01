
State.pokupio = 0
def run():
	r.conf_set('send_status_interval', 10)
	lrucica(0)
	rrucica(0)
	rfliper(0)
	lfliper(0)
	napgold(0)
	nazgold(0)
	r.setpos(-1500+308,-1000+390,90)#r.setpos(-1425,-575,180) # red
	r.speed(120)
	
