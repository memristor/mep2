def run():
	r.intr()
	r.conf_set('send_status_interval', 10)
	r.setpos(-1000,0,0)
	sleep(2)
