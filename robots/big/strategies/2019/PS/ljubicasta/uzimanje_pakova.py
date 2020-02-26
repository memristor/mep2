weight=51
def run():
	r.speed(150)
	with _parallel():    
		lift(1,'sredina',0)
		lift(2,'sredina',0)
	r.goto(-1100-20-20-5-10-5-3,250-20+15+5+3)
	x,y=coord('slot_2_1')
	r.goto(x+4-6+2+3,y+6+3+3,1)#kupi prva 3
	r.absrot(0)
	_sync()
	pump(1,1)
	sleep(0.05)
	pump(2,1)
	sleep(0.05)
	pump(3,1)
	sleep(1)
	llift(2)
	sleep(1)
	_sync()
	llift(1)	
	lift(2,'pri_vrhu', 1)
	sleep(0.1)
	r.speed(50)  #bilo 100, proklizava
	r.turn(180)

	# nakon okreta

	r.speed(150) #bilo 150, proklizava
	x,y=coord('slot_2_2')
#r.goto(x+4-4-3-10,y-3-2+9-1+8,-1)#mozda se menja, kupi druga 2
	r.forward(-90)
	r.absrot(180)
	#for i in range(4,7):
	pump(6,1)
	sleep(0.05)
	pump(5,1)
	sleep(1)
	rlift(2)
	sleep(1)
	rlift(1)
	sleep(0.1)
	lift(1,'pri_vrhu', 1)
	r.turn(-10)
	r.forward(-110)
	x,y=coord('slot_2_2_obratno')
	r.goto(x-400,y)
	r.speed(50)  #bilo 90, proklizava
	r.turn(-90)
	r.speed(130) #bilo 130, proklizava
