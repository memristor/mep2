import core.State as State
weight=0

def run():
	combination = State.combination
	
	#####################3
	##  COLLECTING THIRD
	####################

	colors = ['green', 'black', 'orange','blue']
	s=get(colors, combination)

	start_rotation = s[0]
	
	y_third = 525
	
	def set1():
		lift(1)
		rotate(start_rotation)
	_spawn(set1)
	  
	r.goto(-790, y_third, -1) # r.goto(550,-1355,-1)
	r.speed(50)
	with disabled('collision'):
		r.goto(-340, y_third) # r.goto(1000,-1355)
		
		lift(0)
		pump(0,1)
		sleep(0.2)
		lift(1)
	
	r.speed(130) #sa 100
	#r.forward(-150)
	r.goto(-300,y_third)
	r.goto(-500,y_third,-1)
	r.goto(-500, -400) # r.goto(550,-300)
	with disabled('collision'):
		r.goto(-500, -700) # r.goto(550,-120)

	build_cubes(s[1])
	addpts(10)
	
	r.forward(-150)
	#  r.goto(590, -549, -1) # r.goto(750,-300,-1)
