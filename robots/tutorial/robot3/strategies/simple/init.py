def run():
	r.intr()
	r.conf_set('send_status_interval', 10)
	r.setpos(700,750,0)
	r.speed(60)
	sleep(1)
