weight=4
_instances=2
p=[100,300]
def run():
	# not necessary but useful for visualising on gui
	r.conf_set('send_status_interval', 100)
	r.conf_set('accel', 500)
	r.conf_set('alpha', 500)

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

	# wait 1 second
	if _i == 1:
		sleep(1)
	else:
		sleep(5)
		
	# go back to 0,0
	r.goto(0,0)
	
	# go to 200,0
	r.goto(200,0)

	# go back to 0,0 in reverse
	r.goto(0,0,-1)
