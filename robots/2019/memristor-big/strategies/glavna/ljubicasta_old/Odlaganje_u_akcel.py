weight=7
def run():
	#RESETOVANJE y ---------------------------
	r.speed(30)
	def f(): _goto(offset=1, ref='main')
	r.conf_set('enable_stuck', 1)
	_on('motion:stuck', f)
	r.forward(-500)
	r.setpos(y =-971+225)
	r.conf_set('enable_stuck', 0)
	r.goto(0, -510+20,1)

	with _parallel():
		lift(1,'accel')
		lift(2,'accel')
	
	_sync()
	r.speed(140)
	r.curve_rel(-200,-90,-1)
	r.goto(-80,-788-2)

	'''def test_pump(n):
		p = pressure(n)
		@_do
		def _():
			if State.pumpe[n].val != False and p.val == False:
				addpts(State.color_vaga_bodovi[State.pumpe[n].val])
			State.pumpe[n].val = False'''
	r.absrot(180)
	llift(2)
	r.forward(-177)
	r.absrot(180)
	pump(1,0)
	sleep(0.3)
	llift(1)
	r.absrot(180)
	sleep(0.5)
	llift(2)
	r.forward(-100)
	#r.absrot(180)
	pump(2,0)
	sleep(0.3)
	llift(1)
	sleep(0.5)
	llift(2)
	r.forward(-100)
	#r.absrot(180)
	llift(1)
	pump(3,0)
	sleep(0.3)
	llift(1)
	sleep(1)
	r.goto(100,-782-3)
	r.turn(180)
	'''r.forward(180)
	r.absrot(0)
	pump(4,0)
	rlift(1)
	sleep(0.5)'''
	rlift(2)
	r.absrot(0)
	r.forward(280)
	#r.absrot(0)
	pump(6,0)
	sleep(0.5)
	rlift(1)
	sleep(0.5)
	rlift(2)
	r.forward(100)
	pump(5,0)
	sleep(0.5)
	rlift(1)

