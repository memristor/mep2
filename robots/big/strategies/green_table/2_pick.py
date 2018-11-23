weight=5
def run():
	
	colors = ['black', 'green', 'blue','orange']
	s=get(colors, State.combination)

	start_rotation = s[0]
	
	def set1():
		lift(1)
		rotate(start_rotation)
	_spawn(set1)
	
	sleep(0.1)
	r.goto(1190-15, -600) # r.goto(150,-250)
	r.goto(1190-15, -50) # r.goto(150,-800)
	r.speed(50)
	
	with disabled('collision'):
		r.goto(1190, 250) # r.goto(150,-1100) r.goto(1190+15,250)
		pick()
		
	r.speed(130)
	r.goto(1190, -50, -1) # r.goto(150,-800,-1)
	
	r.goto(1010+40+10, -310, -1) # r.goto(330,-390,-1)
	r.goto(1010+50,-550)
	with disabled('collision'):
		r.goto(1010+40+10, -700) #  r.goto(330, -120)
	

	build_cubes(s[1])
	addpts(40)
	#  r.goto(790, -550, -1) # r.goto(550,-300,-1)
	with disabled('collision'):
		r.forward(-150)
	lift(0)
