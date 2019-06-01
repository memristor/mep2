weight = 50
State.pokupio = 0
def run():
	r.conf_set('send_status_interval', 10)

	r.setpos(-1195,-610,90)#r.setpos(-1425,-575,180) # red
	r.speed(120)
	napgold(1)
	nazgold(1)
	
