
weight=10

def run():
	
	lift(0)
	sleep(0.2)
	with _parallel():    
		sgl(2)
		sgd(2)
		sdl(2)
		sdd(2)
	sleep(0.5)
	#lift(1)
	r.speed(120)
	r.turn(25)
	sleep(1)
	r.forward(200)
	with _parallel():    
		sgl(1)
		sgd(1)
	sleep(3)
	r.forward(-200)
	with _parallel():    
		sgl(2)
		sgd(2)
	sleep(100)
