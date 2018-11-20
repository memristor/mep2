weight=10

def run():
	r.speed(170)
	if not pathfind(1269, 845):
		return False
	
	pcelica(2)
	r.goto(1314, 845, -1)
	pcelica(1)
	r.goto(1254, 845)
	addpts(50)

def leave():
	pcelica(0)
