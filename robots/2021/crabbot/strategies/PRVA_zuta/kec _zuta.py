
weight=10

def run():
	
	#otvaranje gripera

	#sgl(2)
	#sleep(0.2)
	#sgd(2)
	#sleep(0.2)
	#lift(1)
	#sgl(1)
	#sleep(0.2)
	#sdd(0)	
	#sleep(0.2)
	#sdl(0)	
	#r.speed(150)
	#sleep(20)
#################
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
	#sleep(20)
	
	r.curve_rel(-652, 43)#650 40
	r.forward(10)
	with _parallel():
		sgd(1)
		sgl(1)
	sleep(0.6)
	#r.curve_rel(20, -15)#650 40
	#r.forward(28)
	r.speed(170)
	#sleep(0.2)
	with _parallel():	
		lift(1)
		r.curve_rel(-1150, 90)
	sleep(1.8)
	sdl(1)
	sleep(0.2)
	r.goto(-470,310)#zelena sredina
	sdd(1)
	sleep(0.2)	
	sdl(2)
	sleep(0.2)
	r.curve_rel(1250, 50)
	r.goto(150, -1000+540+10)#priprema za luku
	sleep(0.2)
	r.speed(80)
	r.turn(-45)
	r.forward(300)
	with _parallel():	
		sdd(2)
		sdl(2)
	sleep(0.2)
	sleep(0.4)
	r.forward(-120)
	sleep(0.4)
	lift(0)
	sleep(0.4)
	with _parallel():	
		sgd(2)
		sgl(2)
	sleep(0.4)
	r.forward(-240)
	r.turn(18)
	r.forward(190)
	r.turn(-27)
	r.forward(-240)
	r.goto(0,0)
	r.turn(360)
	r.turn(-360)
	sleep(20)#0.2
	#zatvaraju se gornji griperi
	#gornji griperi idu gore
	#r.curve_rel(500, 45)#350 45
	#paralelno dizemo donje gripere
	#r.turn(60)
	#sleep(0.2)
	
	r.goto(1500-920+180, 600+70)# zelena kompas
	sleep(0.5)
	r.absrot(180)
	sleep(0.2)
	r.forward(100)
	sleep(0.2)
	sdd(1)
	sleep(0.2)
	r.goto(450,300)#crvena sredina
	sleep(0.2)
	r.absrot(-90)
	sleep(0.2)
	r.forward(50)
	sdl(1)
	sleep(0.2)
	r.goto(1500-1265+70, -200+210+40)#zelena 2
	sleep(0.2)
	sdd(2)
	sleep(0.2)
	#r.turn(-20)
	sleep(0.2)
	r.turn(7)
	sleep(0.2)
	r.forward(300)
	sleep(0.2)
	r.goto(-1500+1240, -1000+540+100)#priprema za luku
	sleep(0.2)
	r.absrot(-90)
	sleep(0.2)
	r.forward(415)
	sleep(0.2)
	sdl(1)
	sleep(0.2)
	sdl(2)
	r.forward(-120)
	sleep(0.2)
	lift(0)
	sleep(0.2)
	with _parallel():
		sgl(2)
		sgd(2)
	sleep(0.5)
	r.forward(-220)
	sleep(20)#0.5
	#otvaranje gripera/aktivacija svetionika

	r.forward(-230)

	sleep(0.5)
	r.curve_rel(-430, 90)
	r.forward(30)
	#sleep(0.5)
	r.curve_rel(-1300, 30)
	#r.absrot(90)

	r.curve_rel(-590, 80)
	#sleep(1)
	r.curve_rel(600, 105)
	r.curve_rel(-1400, 25)
	r.curve_rel(-950, 60)
	r.forward(130)
	sleep(0.3)
	##otvaraju se donji griperi
	r.forward(-80)
	sleep(0.3)
	##gornji griperi silaze i otvaraju se
	r.forward(-120)
	sleep(3)
