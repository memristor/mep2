# weight=4
def run():	
	
	sleep(2)
	x,y = coord('priprema_akcelerator_1')
	r.curve_rel(570,-90,-1)
	#r.goto(0,-550-30,-1)
	r.goto(x,y-30,-1)
	r.absrot(90)
	
	r.speed(30)
	def f():
		_goto(offset=1, ref='main')
	r.conf_set('enable_stuck', 1)
	_on('motion:stuck', f)
	r.forward(-500)
	r.setpos(y =-971+225)
	r.conf_set('enable_stuck', 0)
	
	#r.goto(0, -550,1)
	r.goto(*coord('priprema_akcelerator_1'))
	with _parallel():
		lift(1,'accel')
		lift(2,'accel')
	
	_sync()
	
	r.speed(160)
	r.curve_rel(-200,-90,-1)
	
	#first
	#r.goto(80,-788)
	r.goto(*coord('priprema_akcelerator_2_1'))
	
	r.absrot(0)
	llift(2)
	x,y=coord('priprema_akcelerator_2_1')
	#r.forward(-180)#200
	r.goto(x-180,y,-1)
	pump(4,0)
	llift(1)
	sleep(0.5)
	
	def test_pump(n):
		p = pressure(n)
		@_do
		def _():
			if State.pumpe[n].val != False and p.val == False:
				addpts(State.color_vaga_bodovi[State.pumpe[n].val])
			State.pumpe[n].val = False

	test_pump(4)

	
	llift(2)
	#r.forward(-100)
	r.goto(x-280,y,-1)
	pump(5,0)
	llift(1)
	sleep(0.5)

	test_pump(5)
	
	llift(2)
	#r.forward(-100)
	r.goto(x-380,y,-1)
	llift(1)
	pump(6,0)
	sleep(0.5)

	test_pump(6)
	rlift(1)
	#second
	
	sleep(1)
	#r.goto(-100,-782)
	r.goto(*coord('priprema_akcelerator_2_2'))
	r.absrot(180)
	x,y = coord('priprema_akcelerator_2_2')
	#r.forward(200)
	r.goto(x-200,y)
	pump(1,0)
	rlift(1)
	sleep(0.5)
	test_pump(1)
	
	rlift(2)
	#r.forward(100)
	r.goto(x-300,y)
	pump(2,0)
	test_pump(2)
	rlift(1)
	sleep(0.5)
	rlift(2)
	#r.forward(100)
	r.goto(x-400,y)
	
	pump(3,0)
	rlift(1)
	test_pump(3)
