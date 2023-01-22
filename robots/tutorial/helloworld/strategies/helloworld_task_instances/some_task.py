weight=4
_instances=2
p=[100,300]
def run():
	# not necessary but useful for visualising on gui
	r.conf_set('send_status_interval', 10)
	r.conf_set('accel', 500) # robot accelerates to given speed 100 for 500ms
	r.conf_set('alpha', 500) # robot accelerates (rotation) to given speed 100 for 500ms
	
	r.speed(100)

	# natural mathematic coordinate system
	# x - when robot orientation == 0, robot is looking at positive x axis
	# y - when robot orientation == 90, robot is looking at positive y axis
	r.setpos(0,0,0)
	
	# 200 mm forward
	r.forward(p[_i])

	# 200 mm backward
	r.forward(-p[_i])

	# move to point 200,200
	r.goto(200,200)

	if _i == 1:
		# task #0 will wait 1 second
		sleep(1)
	else:
		# task #1 will wait 5 seconds
		sleep(5)
		
	# go back to 0,0
	r.goto(0,0)
	
	# go to 200,0
	r.goto(200,0)

	# go back to 0,0 in reverse
	r.goto(0,0,-1)
