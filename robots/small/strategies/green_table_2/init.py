def run():
	r.conf_set('status_interval',100)

	r.conf_set('send_status_interval', 100)
	r.conf_set('enable_stuck', 1)
	r.conf_set('wheel_r1', 68.0)
	r.conf_set('wheel_r2', 67.25513)
	r.conf_set('wheel_distance', 252.30)

	r.conf_set('pid_d_p', 2.75)
	r.conf_set('pid_d_d', 60)
	#r.conf_set('pid_r_p', 1.5)
	r.conf_set('pid_r_p', 1.2)
	r.conf_set('pid_r_d', 100)

	r.conf_set('pid_r_i', 0.01)
	r.conf_set('accel', 700)
	    
	wait_activator()

