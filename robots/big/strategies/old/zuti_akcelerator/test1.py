#weight=2
def run():
	r.speed(150)

	with _parallel():
		llift(0)
		rlift(0)
		lift(2,'pri_vrhu')
		lift(1,'pri_vrhu')
	#r.forward(60)
	r.goto(-1215,370,-1)
	r.goto(-795,355)#kupi prva 3
	sleep(1)

	for i in range(1,4):
		pump(i,1)
	llift(2)
	sleep(2)
	lift(2,'pri_vrhu', 1)
	llift(1)	
	sleep(0.1)
	r.absrot(0)
	r.turn(180)
	r.goto(-693,355,-1)#mozda se menja, kupi druga 3
	for i in range(4,7):
		pump(i,1)
	rlift(2)
	sleep(0.1)
	lift(1,'pri_vrhu', 1)
	llift(1)
	
	r.forward(-60)
	with _parallel():
		lift(1,'accel',1)
		lift(2,'accel',1)
#_sync()
	sleep(2)
	
	r.curve_rel(570,-90,-1)
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
	
	r.speed(160)
	r.curve_rel(-200,-90,-1)
	r.goto(-80,-788)
	r.absrot(180)
	llift(2)
	r.forward(-200)
	pump(1,0)
	llift(1)
	sleep(0.5)
	llift(2)
	r.forward(-100)
	pump(2,0)
	llift(1)
	sleep(0.5)
	llift(2)
	r.forward(-100)
	llift(1)
	pump(3,0)
	sleep(0.5)
	llift(1)
	sleep(1)
	r.goto(100,-782)
	r.turn(180)
	r.absrot(0)
	r.forward(200)
	pump(4,0)
	rlift(1)
	sleep(0.5)
	rlift(2)
	r.forward(100)
	pump(6,0)
	rlift(1)
	sleep(0.5)
	rlift(2)
	r.forward(100)
	pump(5,0)
	rlift(1)