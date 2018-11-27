weight=10

def run():

	r.speed(100)
	addpts(10)
	r.conf_set('enable_stuck', 0)

	colors = ['black', 'green', 'blue', 'orange']
	r,b=get(colors, State.combination)

	start_rotation = r
	
	def prepare_cross():
		lift(1)
		rotate(start_rotation)
		_label('prepared')
	_spawn(prepare_cross)
	
	with disabled('collision'):
		#zeki ugasio za prvi krst nema potrebe za senzorima
		r.goto(640, -800) #  r.goto(700, -50)
		r.absrot(90)
		r.speed(60)
		r.goto(640, -400) # r.goto(700, -450)
		_sync('prepared')
		pick()
	
	r.speed(130)
	r.goto(820, -600, -1) # r.goto(700, -150, -1)	#630
	r.goto(820, -700) # r.goto(700, -150, -1)	#630
	#  r.turn(180)
	
	#  r.turn(180)
	build_cubes(b)
	addpts(40)	
	r.forward(-150)
	
