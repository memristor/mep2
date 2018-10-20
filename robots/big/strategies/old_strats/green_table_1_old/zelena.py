weight=3

def run():
	print('starting task')
	sleep(10)
	def build_cubes(color):
		for i in enumerate(color):
			lift(max(1, i[0]))
			unload(i[1],i[0] == 0)
		lift(3)
		unload(get_remaining_pump(color))

	addpts(0)
	r.setpos(80,-350, 0)

	r.conf_set('accel', 800)
	r.conf_set('alpha', 800)
	r.speed(120)
	
	addpts(10)
	#  r.conf_set('stuck_enabled', 0)

	#combination = ['blue','green','orange']
	#combination = ['blue','orange','black']
	#combination = ['black','orange','blue']
	#  combination = ['black','blue','green']
	#combination = ['black','yellow','orange']
	#combination = ['green','orange','yellow']
	#combination = ['green','yellow','blue']
	#combination = ['orange','blue','yellow']
	#combination = ['orange','black','green']    
	#  combination = ['yellow','black','blue']
	#  combination = ['yellow','green','black']
	combination = ['black', 'blue', 'green']
	
	colors = ['green', 'blue', 'orange','black']
	s=get(colors, combination)

	start_rotation = s[0]
	lift(1)
	rotate(start_rotation)

	r.goto(1140, -310) #  r.goto(200, -390)
	r.goto(40, -309) # r.goto(1300, -390)
	#sleep(1)
	lift(0)
	pump(0,1)
	sleep(1)
	lift(1)
	#r.forward(800)
	#r.forward(-700)
	r.goto(1010, -310, -1) # r.goto(330,-390,-1)
	r.goto(1010, -580) #  r.goto(330, -120)

	build_cubes(s[1])
	addpts(40)
	r.goto(1010, -450, -1) # r.goto(330 ,-250,-1)
	########################
	##STUCK
	#########################
	#  r.conf_set('enable_stuck', 0)
	r.goto(1290, -450, -1) # r.goto(50,-250,-1)
	r.speed(20)
	r.goto(1350, -450, -1) # r.goto(-10  ,-250,-1)
	sleep(0.2)
	r.setpos(x=1260)
	r.speed(100)

	########################


	colors = ['black', 'green', 'blue', 'orange']
	s=get(colors, combination)

	start_rotation = s[0]
	lift(1) 
	rotate(start_rotation)
	
	sleep(0.1)
	r.goto(1190, -450) # r.goto(150,-250)
	r.goto(1190, 100) # r.goto(150,-800)
	r.speed(50)
	r.goto(1190, 400) # r.goto(150,-1100)
	lift(0)
	pump(0,1)
	sleep(0.5)
	lift(1)
	r.speed(100)
	r.goto(1190, 100, -1) # r.goto(150,-800,-1)
	r.goto(790, -399) # r.goto(550,-300)
	r.goto(790, -580) # r.goto(550,-120)

	build_cubes(s[1])
	addpts(40)
	r.goto(790, -399, -1) # r.goto(550,-300,-1)

	#####################3
	##  COLLECTING THIRD
	####################

	colors = ['green', 'blue', 'orange','black']
	s=get(colors, combination)

	start_rotation = s[0]
	lift(1)
	rotate(start_rotation)
	  

	r.goto(790, 655, -1) # r.goto(550,-1355,-1)
	r.goto(340, 655) # r.goto(1000,-1355)
	lift(0)
	pump(0,1)
	sleep(0.2)
	lift(1)
	r.goto(590, 655, -1) # r.goto(750,-1355,-1)
	r.goto(590, -579) # r.goto(750,-120)

	build_cubes(s[1])
	addpts(40)
	addpts(125)
	r.goto(590, -399, -1) # r.goto(750,-300,-1)
	lift(0)
