#green
import core.State as State
weight=10

def run():
	combination = State.combination

	r.speed(150)#zeki ubrzao sa 100
	addpts(10)
	r.conf_set('enable_stuck', 0)

	colors = ['orange','black', 'green', 'blue']
	s=get(colors, combination)

	start_rotation = s[0]
	
	def set1():
		lift(1)
		rotate(start_rotation)
	_spawn(set1)
	r.goto(600,-460) # brze pa uspori
	with disabled('collision'):
		#zeki ugasio za prvi krst nema potrebe za senzorima
		#r.goto(640, -770) #  r.goto(700, -50)
		r.speed(60)
		r.goto(640, -460) # r.goto(700, -450)
	
	with disabled('collision'):
		lift(0)
		pump(0,1)
		sleep(1)
		lift(1)
	
	r.speed(70) #istovar
	r.goto(300, -460) # r.goto(700, -150, -1)
	r.goto(640, -460, -1) # r.goto(700, -150, -1)
	r.goto(640,-700)
	#  r.turn(180)
	
	#  r.turn(180)
	build_cubes(s[1])
	addpts(40)	

	r.forward(-150)
	return
	
	########################
	##STUCK
	#########################
	r.conf_set('enable_stuck', 0)
	r.goto(1290, -600, -1) # r.goto(50,-250,-1)
	r.speed(20)
	r.goto(1350, -600, -1) # r.goto(-10  ,-250,-1)
	sleep(0.2)
	r.setpos(x=1260)
	
	r.speed(100)
	

	########################


	
	  
	

	
