#orange
import core.State as State
weight=10
#NARANDZASTA
def run():
	combination = State.combination

	r.speed(120) #zeki
	addpts(10)
	r.conf_set('enable_stuck', 0)

	colors = ['orange','blue', 'green', 'black']
	s=get(colors, combination)

	start_rotation = s[0]
	
	def set1():
		lift(1)
		rotate(start_rotation)
	_spawn(set1)
	
	# zeki dodaje fali bre
	with disabler('collision'):
		r.speed(60) # sa 60 ZEKI
		r.goto(-640, -460) # r.goto(700, -450)	

	
	with disabler('collision'):
		lift(0)
		pump(0,1)
		sleep(1)
		lift(1)
	
	r.speed(130) # sa 50 digao
	#r.absrot(0)
	r.goto(-640, -300) # r.goto(700, -150, -1) #-300,-460
	r.goto(-640, -460,-1) # r.goto(700, -150, -1)	
	r.speed(50)	
	r.goto(-640,-700)
	
	build_cubes(s[1])
	addpts(10)
	
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


	
	  
	

	
