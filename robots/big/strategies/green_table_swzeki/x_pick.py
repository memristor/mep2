import core.State as State
weight=6

def run():
	tower_pos=600
	combination = State.combination
	
	#####################3
	##  COLLECTING 1 na drugoj a ovo je od 3 ce
	####################
	r.speed(150)
	colors = ['orange', 'blue', 'green','black']
	s=get(colors, combination)

	start_rotation = s[0]
	
	def set1():
		lift(1)
		rotate(start_rotation)
	_spawn(set1)
	 # adresa protivnikove 
	r.goto(640,-460, -1) # r.goto(550,-1355,-1)
	r.absrot(180)
	r.goto(-590,-460)
	r.speed(50)#usopori prilaz
	with disabler('collision'):
		r.goto(-680,-460)#640 bi trebalo
		
		lift(0)
		pump(0,1)
		sleep(0.2)
		lift(1)
	
	r.speed(100)
	r.forward(-150)
	r.absrot(0)
	
	r.goto(400,-460) # r.goto(550,-300)
	with disabler('collision'):
		r.goto(tower_pos, -500)
		r.goto(tower_pos, -700)
	build_cubes(s[1])
	addpts(40)
	
	r.forward(-150)
	#  r.goto(590, -549, -1) # r.goto(750,-300,-1)
