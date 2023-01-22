weight = 50
State.pokupio = 0
def run():
	r.conf_set('send_status_interval', 10)

	r.setpos(-1500+308,-1000+390,90)#r.setpos(-1425,-575,180) # red
	r.speed(80)
	
