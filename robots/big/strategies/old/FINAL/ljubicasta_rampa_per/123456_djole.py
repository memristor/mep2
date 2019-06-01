weight=5
def run():
	#ljubicata
	r.speed(200)

	with _parallel():
		llift(0)
		rlift(0)
		lift(2,'sredina')
		lift(1,'sredina')
	sleep(0.1)

	#r.forward(60)
	r.goto(1200,200,-1)
	r.goto(-795,360,1)#kupi prva 3 355
	r.absrot(0)
	sleep(1)
	_sync()
	for i in range(1,4):
		pump(i,1)
	llift(2)
	_sync()
	lift(2,'sredina', 1)
	llift(1)	
	sleep(0.1)
	r.absrot(0)
	r.turn(180)
	r.goto(-693,355,-1)#mozda se menja, kupi druga 3
	for i in range(4,7):
		pump(i,1)
	rlift(2)
	sleep(0.1)
	lift(1,'sredina', 1)
	llift(1)
	
	
	r.forward(-200)
	r.turn(9)
	r.forward(400)
	
	# r.curve_rel(570,-90,-1)
	# r.goto(0,-550-30,-1)
	# r.absrot(90)
	
	
	return
