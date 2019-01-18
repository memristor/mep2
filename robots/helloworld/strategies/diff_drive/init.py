def run():
	# r.setpos(0,0,0)
	r.diff_drive(100,300, -45)
	r.diff_drive(100,-300, -45)
	r.diff_drive(-100,300, 180)
