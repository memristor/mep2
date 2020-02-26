weight=1
def run():
	#-----------------------------------------------------------------------------
	#isporuka plavog
	r.speed(80) ############################### smanjeno sa 100 na 50 zbog klizanja
	#r.forward(-40)
	r.absrot(45)
	_print('priprema')
	with _while(lambda: State.PS_mali.val == 1):
		@_do
		def _():
			_print('cekam', State.PS_mali.val)
	_print('nastavljam')
	State.PS_veliki.val=1
	#r.goto(-900,1000-60-620-40,-1)
	r.forward(-100)
	r.speed(90)
	r.absrot(200)
	rfliper(2)
	r.speed(150)
	r.forward(325)
	r.speed(120)
	r.absrot(270)
	#r.turn(90)

	#x = -1500+(450+150)
	
	with _parallel():    
		lift(1,'dole',0)
		lift(2,'dole',0)
	
	with _parallel():
		rlift(2)
		llift(2)
		
		
	r.forward(550)
	r.curve_rel(50*2,120)
	r.forward(150)
	addpts(13) #ugurana 2c i 1z pak
	r.forward(-150)
	r.curve_rel(50*2,-120)
	r.absrot(270)
	r.forward(50)
	
	@_core.do
	def check_pts(idx):
		p = pressure(idx)
		@_do
		def _():
			if p.val == 1:
				addpts(6)
	
	# crvena (2)
	check_pts(2)
	pump(2,0)
	#addpts(6)
	sleep(0.7)
	r.forward(-150)
	sleep(0.5)
	
	
	# zelena (1)
	check_pts(1)
	pump(1,0)
#	addpts(6)
	sleep(0.7)
	
	
	# zelena (6)
	addpts(6)
	r.absrot(90)
	r.forward(200)
	sleep(0.5)
	pump(6,0)
	sleep(0.7)
	r.turn( 20)
	r.turn(-20)
	
	
	# crvena (5)
	r.forward(-150)
	check_pts(5)
	pump(5,0)
	sleep(0.5)
	r.turn(20)
	r.turn(-20)
	
	# crvena (4)
	r.forward(-150)
	check_pts(4)
	pump(4,0)
	#addpts(6)
	sleep(0.5)
#	r.turn(20)
#	r.turn(-20)
	
	
	
	
	rfliper(0)
	r.speed(140)
	r.forward(800)
	r.absrot(45)
	r.goto(1246,340)
	State.PS_veliki.val=0
	
	
	
	
	#@_spawn
	#def _():
		#rfliper(2)
	#lfliper(2)
	#sleep(2)
	
	#r.curve_rel(650, 45)
	#r.turn(40)
	#r.forward(120)
	#r.forward(-120)
	# r.turn(-40)
	# r.forward(-300)
	# r.forward(500)
	# r.absrot(45)
	# r.forward(250)
	#State.PS_veliki.val=0
	# r.absrot(90)
	# r.forward(150)
	
	
