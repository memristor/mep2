weight=1
def run():
	r.speed(60)
	# r.curve_rel(100,180)
	# sleep(1)
	# r.curve_rel(100,-180)
	# sleep(1)
	# r.curve_rel(-100,180)
	# sleep(1)
	# r.curve_rel(-100,-180)
	
	
	r.curve(100,0,180)
	sleep(1)
	r.curve(100,0,-180)
	sleep(1)
	r.curve(100,0,180)
	sleep(1)
	r.curve(100,0,-180)
	
