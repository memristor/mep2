weight=5
mali = _State(0, name='mali', shared=True)
def run():
	#zuta
	r.speed(100)
	addpts(400)
	with _parallel():
		llift(0)
		rlift(0)
		lift(2,'sredina')
		lift(1,'sredina')
		
	r.goto(1200,200,-1)#MINUS JEDAN IDE kad ida i rampa
	r.goto(795,355)#kupi prva 3
	
	r.absrot(180)
	_sync()
	for i in range(4,7):
		pump(i,1)
	rlift(2)
	lift(1,'sredina', 1)
	rlift(1)	
	sleep(0.1)
	#r.absrot(0)
	r.turn(-180)
	r.goto(698,355,-1)#mozda se menja, kupi druga 3   693
	for i in range(1,4):
		pump(i,1)
	llift(2)
	sleep(0.1)
	lift(2,'sredina', 1)
	llift(1)
	
	r.forward(-60)
	
	with _parallel():
		lift(1,'accel',1)
		lift(2,'accel',1)
#_sync()
	return
	
	
