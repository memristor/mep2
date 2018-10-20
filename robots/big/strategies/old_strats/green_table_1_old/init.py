def run():
	r.conf_set('send_status_interval', 100)
	r.conf_set('wheel_distance', 255.2) #248.47
	#r.conf_set('wheel_r1', 63.35) # smanjivanje => ide ulevo
	#r.conf_set('wheel_r1', 63.55)
	#r.conf_set('wheel_r2', 64.2)
	r.conf_set('wheel_r1', 63.67) #61.92
	r.conf_set('wheel_r2', 64)  
	r.conf_set('pid_d_p', 3.7)
	r.conf_set('pid_d_d', 100)
	r.conf_set('pid_r_p', 4.0)
	r.conf_set('pid_r_d', 150)
	r.conf_set('pid_r_i', 0.013)
	r.conf_set('accel', 600)
	r.conf_set('alpha', 1000)
	#  wait_activator()
	#sleep(10)
