weight=51
def run():
	r.speed(130)
	with _parallel():    
		lift(1,'dole',0)
		lift(2,'dole',0)
	r.goto(1100+20+20+5+10+5+3+1+1,250-20+15+5+3+1+1)
	x,y=coord('slot_2_1')
	r.goto(x-6,y-6+2,1)#kupi prva 3
	r.absrot(130)
	_sync()
	pump(4,1)
	sleep(0.05)
	pump(5,1)
	sleep(0.05)
	pump(6,1)
	sleep(0.2)
	rlift(2)
	sleep(0.8)
	_sync()
	rlift(1)
	lift(1,'pri_vrhu', 1)	
	sleep(0.1)
	r.speed(70)
	r.turn(-180)
	r.speed(140)
	x,y=coord('slot_2_2')
	r.goto(x,y-2-6-5-2+1+1+1+2+1+2+1,-1)#mozda se menja, kupi druga 2
	r.absrot(0)
	#for i in range(4,7):
	pump(2,1)
	sleep(0.05)
	pump(1,1)
	sleep(0.2)
	llift(2)
	sleep(0.8)
	llift(1)
	sleep(1)
	lift(2,'pri_vrhu', 1)
	r.turn(7)
	r.forward(-110)
	x,y=coord('slot_2_2_obratno')
	r.goto(x+400,y)
	r.speed(90)
	r.turn(90)
	r.speed(130)