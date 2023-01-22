import core.State as State
weight=5
def run():
	
	colors = ['black', 'orange', 'blue','green']
	s=get(colors, State.combination)

	start_rotation = s[0]
	
	def set1():
		lift(1)
		rotate(start_rotation)
	_spawn(set1)
	
	sleep(0.1)

	r.goto(-1190-10, -600) # r.goto(150,-250)
	'''
	with disabled('collision'):
		r.speed(30)
		r.goto(-1190-3,-870,-1)
		sleep(1)
		r.setpos(y=-845)
	'''
	
	r.speed(130)
	r.goto(-1190-10, -50) # r.goto(150,-800)
	
	r.speed(50)
	
	with disabled('collision'):
		r.goto(-1190-10, 300) # r.goto(150,-1100)
		lift(0)
		pump(0,1)
		sleep(0.5)
		lift(1)
		
	r.speed(130)# sa 100 zeki
	r.goto(-1190, -50, -1) # r.goto(150,-800,-1)
	
	r.goto(-(1010+40+10), -310, -1) # r.goto(330,-390,-1)
	with disabled('collision'):
		r.goto(-(1010+50),-500) #dodato zeki
	r.goto(-(1010+40+10), -700) #  r.goto(330, -120)

	build_cubes(s[1])
	addpts(10)
	#  r.goto(790, -550, -1) # r.goto(550,-300,-1)
	r.forward(-150)
	lift(0)