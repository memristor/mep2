def run():
	r.conf_set('send_status_interval', 10)
	r.setpos(-1500+308,-1000+390,90)#r.setpos(-1425,-575,180) # red
	r.speed(50)
	napgold(0)
	nazgold(1)
	rrucica(0)
	lrucica(0)
	r.speed(50)
