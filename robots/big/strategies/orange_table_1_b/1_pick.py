import core.State as State
weight=10

def run():
	combination = State.combination

	r.speed(100)
	addpts(10)
	r.conf_set('enable_stuck', 0)

	colors = ['black', 'orange', 'blue','green']
	s=get(colors, combination)

	start_rotation = s[0]
	
	def set1():
		lift(1)
		rotate(start_rotation)
	_spawn(set1)

	
	r.goto(-635, -790) #  r.goto(700, -50) bilo 800
	r.absrot(90)
	r.speed(60)
	r.goto(-635, -400) # r.goto(700, -450)
	
	with disabler('collision'):
		lift(0)
		pump(0,1)
		sleep(1)
		lift(1)
	
	r.speed(130)
	r.goto(-630, -600, -1) # r.goto(700, -150, -1)
	r.goto(-630, -700) # r.goto(700, -150, -1)	

	#  r.turn(180)
	
	#  r.turn(180)
	build_cubes(s[1])
	
	r.forward(-150)
	return
	
	########################
	##STUCK
	#########################
	r.conf_set('enable_stuck', 0)
	r.goto(-1290, -600, -1) # r.goto(50,-250,-1)
	r.speed(20)
	r.goto(-1350, -600, -1) # r.goto(-10  ,-250,-1)
	sleep(0.2)
	r.setpos(x=-1260)
	
	r.speed(100)

	########################


	
	  
	

	
