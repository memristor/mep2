weight=8
def run():
	x,y=coord('slot_2_2')
	with _parallel():
		lift(1,'accel',1)
		lift(2,'accel',1)
		r.goto(x+60+50,y-50+10,-1)
	_sync()
	
	r.absrot(180)
	r.curve_rel(570,-90,-1)
	r.goto(0,-550-70,-1)
	r.absrot(90)
	
	
