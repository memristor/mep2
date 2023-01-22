weight=2
def run():
	# not necessary but useful for visualising on gui
	r.conf_set('send_status_interval', 10)
	
	# natural mathematic coordinate system
	# x - when robot orientation == 0, robot is looking at positive x axis
	# y - when robot orientation == 90, robot is looking at positive y axis
	r.setpos(0,0,0)

	# 200 mm forward
	r.forward(200)

	# 200 mm backward
	r.forward(-200)

	# move to point 200,200
	r.goto(200,200)

	# wait 1 second
	sleep(1)

	# go back to 0,0
	r.goto(0,0)

	# go to 200,0
	r.goto(200,0)

	# go back to 0,0 in reverse
	r.goto(0,0,-1)
