weight=51
def run():
	r.speed(80) ############################### smanjeno sa 200 na 50 zbog klizanja
	with _parallel():    
		lift(1,'dole',0)
		lift(2,'dole',0)
	r.goto(1100+20+20+5+10+5+3+1+1-4,250-20+15+5+3-3)
	x,y=coord('slot_2_1')
	r.goto(x-6+2-4-4,y-6-1+4,1)#kupi prva 3
	r.absrot(180)
	_sync()
	pump(4,1)
	sleep(0.05)
	pump(5,1)
	sleep(0.05)
	pump(6,1)
	sleep(1)
	rlift(2)
	sleep(1)
	_sync()
	rlift(1)
	lift(1,'pri_vrhu', 1)	
	sleep(0.1)

	r.turn(-180)
	x,y=coord('slot_2_2')
#r.goto(x-4+3,y-1-2-6-5-2+1+1+1+2+1+2+1+1+1+2-2-2-2,-1)#mozda se menja, kupi druga 2
	r.absrot(0)
	r.forward(-95)
	r.absrot(0)
	#for i in range(4,7):
	pump(2,1)
	sleep(0.01)
	pump(1,1)
	sleep(0.01)
	pump(3,0)
	sleep(1)
	llift(2)
	sleep(1)
	llift(1)
	sleep(1)
	lift(2,'pri_vrhu', 1)
	r.turn(10)
	r.forward(-120)
	x,y=coord('slot_2_2_obratno')
	r.goto(x+400,y)
	r.speed(70)############################### smanjeno sa 90 na 50 zbog klizanja
	r.turn(90)
	r.speed(120)############################### smanjeno sa 150 na 50 zbog klizanja
