weight=1
def run():
	r.setpos(0,0,0)
	# sleep(1)
	r.speed(100)
	for i in range(3):
		r.curve(500,0, 180, 1)
		# r.turn(180)
		# r.curve_rel(100, 180)
