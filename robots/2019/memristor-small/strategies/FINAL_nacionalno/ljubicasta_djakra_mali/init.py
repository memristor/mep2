weight = 50
def run():
	r.conf_set('send_status_interval', 10)

	#r.setpos(-1425,-575,180) # red
	#r.setpos(-1195,-610, 90) # normalan
	r.setpos(-1195,-610, -90) # obrnuti set pos 
	r.speed(120)
	