def run():
	r.conf_set('send_status_interval', 10)
	r.forward(200)
	r.forward(-200)
