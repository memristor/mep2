
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
	r.forward(870)
	with _parallel():
		sgl(1)
		r.forward(705)
	sleep(2)
	r.turn(-40)
	r.forward(80)
	sgd(1)
	with _parallel():
		lift(1)
		r.absrot(-90)
	sleep(1.5)
	r.turn(10)
	r.forward(400)
	#sdl(1)
	r.turn(-27)
	r.forward(390)
	r.speed(80)
	r.turn(7)
	r.forward(205)
	with _parallel():    
		sdl(2)
		sdd(2)
	r.absrot(-90)
	r.forward(-100)
	lift(0)
	with _parallel():    
		sgl(2)
		sgd(2)
	sleep(0.2)
	r.forward(-110)
	with _parallel():    
		sdl(1)
		sdd(1)
	sleep(0.2)
	r.forward(-125)
	with _parallel():    
		sgl(2)
		sgd(2)
		sdl(2)
		sdd(2)
		r.turn(135)
	sleep(2)
	r.forward(1000)
