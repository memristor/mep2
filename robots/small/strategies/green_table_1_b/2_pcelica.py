weight=10

def run():
	#  r.goto(934, 285) # r.goto(1200,430)
	#pathfind(934, 285) # r.goto(1200,430)
	sleep(0.05)
	#  r.goto(1269, 685) # r.goto(1600,95)
	#  r.goto(1269, 845) # r.goto(1760,95)
	addpts(20)
	if not pathfind(1269, 845): # r.goto(1760,95)
		return False
	#  r.turn(-90)
	pcelica(2)
	r.goto(1314, 845, -1) # r.goto(1760,50,-1) sa 1314 na 1300j
	pcelica(1)
	r.goto(1254, 845) # r.goto(1760,110)
	

def leave():
	pcelica(0)