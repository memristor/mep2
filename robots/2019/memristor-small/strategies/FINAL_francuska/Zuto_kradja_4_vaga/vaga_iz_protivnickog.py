weight = 9
#Nakon sto ukrades pakove 1-6 stavlja u zutu vagu
def run():
	'''if State.pokupio == 0:
		pump(1,0)
		return'''
	r.goto(-200,330,-1)
	r.absrot(90)
	nazgold(1)
	r.curve_rel(-200, -180)
	
	def f():
		_goto(offset=1, ref='main')
	r.conf_set('enable_stuck', 1)
	_on('motion:stuck', f)
	r.goto(200-20,470,-1)
	r.speed(50)
	r.forward(-100)
	r.conf_set('enable_stuck', 0)
	pump(1,0)
	addpts(12)
	sleep(0.5)
	r.goto(200,210,1)

	'''r.goto(-200,470,-1)
	pump(1,0)
	r.goto(-200,325,1)'''
