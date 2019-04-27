weight=4
def run():	
	
	sleep(2)
	r.curve_rel(-570,-90,-1)
	r.goto(0,-550-30,-1)
	r.absrot(90)
	
	#RESETOVANJE y ---------------------------
	r.speed(30)
	def f():
		_goto(offset=1, ref='main')
	r.conf_set('enable_stuck', 1)
	_on('motion:stuck', f)
	r.forward(-500)
	r.setpos(y =-971+225)
	r.conf_set('enable_stuck', 0)
	r.goto(0, -550,1)
	
	with _parallel():
		lift(1,'accel')
		lift(2,'accel')
	
	_sync()
	r.speed(160)
	r.curve_rel(200,-90,-1)
	return
