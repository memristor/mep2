import core.State as State
#weight=9

def run():
	combination = State.combination
	
	#####################3
	##  COLLECTING THIRD
	####################
	r.speed(120) #zeki dodao
	colors = ['green', 'black', 'orange','blue']
	s=get(colors, combination)

	start_rotation = s[0]
	
	def set1():
		lift(1)
		rotate(start_rotation)
	_spawn(set1)
	  
	r.goto(-790, 505-5-3, -1) # r.goto(550,-1355,-1)
	r.speed(50)
	with disabler('collision'):
		r.goto(-340, 505-5-3) # r.goto(1000,-1355)
		lift(0)
		pump(0,1)
		sleep(0.2)
		lift(1)
	
	r.speed(130)
	#r.forward(-150)
	r.forward(-300)
	r.goto(-(790+55), -400) # r.goto(550,-300)
	with disabler('collision'):
		r.goto(-(790+55), -700) # r.goto(550,-120)

	build_cubes(s[1])
	addpts(10)
	
	r.forward(-150)
	#  r.goto(590, -549, -1) # r.goto(750,-300,-1)
