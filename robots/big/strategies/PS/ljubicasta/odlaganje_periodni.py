weight=1
def run():
	#-----------------------------------------------------------------------------
	#isporuka plavog
	r.speed(80) ############################### smanjeno sa 100 na 50 zbog klizanja
	#r.forward(-40)
	r.absrot(135)
	with _while(lambda: State.PS_mali.val == 1):
		pass
	State.PS_veliki.val=1
	#r.goto(-900,1000-60-620-40,-1)
	r.forward(-100)
	r.absrot(340)
	lfliper(2)
	r.speed(150)
	r.forward(325)
	r.speed(60)
	r.absrot(270)
	#r.speed(100)
	#r.turn(90)

	#x = -1500+(450+150)
	
	with _parallel():    
		lift(1,'dole',0)
		lift(2,'dole',0)
		
	
	with _parallel():
		rlift(2)
		llift(2)
	
	r.forward(550)
	#r.absrot(80)
	#r.absrot(180)
	r.curve_rel(-50*2,120)
	r.forward(150)
	addpts(13) #ugurana 2c i 1z pak
	r.forward(-150)
	r.curve_rel(-50*2,-120)
	r.absrot(270)
	#r.speed(150)
	r.forward(50)
	
	@_core.do
	def check_pts(idx):
		p = pressure(idx)
		@_do
		def _():
			if p.val == 1:
				addpts(6)
		
	# crvena (6)
	addpts(6) #BILO check_pts(6) ALI SENZOR NE RADI !!!!
	pump(6,0)
	#addpts(6)
	sleep(0.5)
	
	
	# zelena (5)
	r.forward(-150)
	check_pts(5)
	pump(5,0)
	#addpts(6)
	sleep(0.5)
	
	
	
	r.speed(60)
	r.absrot(90)
	#r.speed(150)
	#r.forward(300)
	
	# zelena (2)
	r.forward(200)
	check_pts(2)
	pump(2,0)
	#addpts(6)
	sleep(0.5)
	r.turn(-20)
	r.turn(20)
	
	
	# crvena (1)
	r.forward(-150)
	check_pts(1)
	pump(1,0)
	#addpts(6)
	sleep(0.5)
	r.turn(-20)
	r.turn(20)
	
	# crvena (3)
	r.forward(-150)
	check_pts(3)
	pump(3,0)
	#addpts(6)
	sleep(0.5)
	r.turn(-20)
	r.turn(20)
	
	
	
	rfliper(0)
	
	r.speed(140)
	r.forward(800)
	r.absrot(135)
	lfliper(0)
	r.goto(-1246, 340)
	# r.forward(450)
	State.PS_veliki.val=0
	# r.absrot(90)
	# r.forward(150)
