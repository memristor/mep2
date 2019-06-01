#weight = 3 #Radi kako treba
#def run():
mali = _State(0, name='mali', shared=True)
weight = 2
def run():

	# Pak za guranje 1300cm od ivice, 774
	# Pak za guranje: (200,1000)
	# Goldium: (726,1000)
	#r.curve_rel(180, -140)
	#r.speed(120)
	#r.goto(-140,-775,-1)
	#r.goto(80,40,-1)
	#r.goto(80,190,-1)
	#r.absrot()
	
	'''_label('back')
	@_do
	def _():
		if not mali.val:
			_goto('back', ref='main')''' #komentarisano zbog testiranjazak
	
	#sleep(10)  	

	@_spawn
	def _():
		lfliper(2)
	rfliper(2)	
	

	
	r.goto(652,-20)		# Valjalo bi da se uradi sa dva kretanja da bi pokupio sve pakove

	r.curve_rel(-500,48)

	#r.goto(-350, 172)
	#r.goto(-600, -78) 
	#@_spawn
	#def _():
	#lfliper(1)
	#rfliper(1)
	#r.goto(-716,-90)
	#r.goto(1000, -550) 
	#r.goto(-1100,-550) #r.goto(-1270,-550)

	r.curve_rel(350,34)
	
	r.forward(-300)
	
	
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)	
	
	# Bodovi kada su svi pakovi u crvenom polju
	addpts(20)
	
	return
	


	



	'''# Pak za guranje 1300cm od ivice, 774
	# Pak za guranje: (200,1000)
	# Goldium: (726,1000)
	#nazgold(0)
	#napgold(0)
	#lfliper(0)
	#rfliper(0)
	#rrucica(0)
	#lrucica(0)

	r.curve_rel(180, -140)
	
	r.speed(100) #POVECATIIII posle kurve
	'''
	'''r.goto(-1195,-775,-1)
	r.absrot(-180)'''
	'''

	#r.goto(-140,-775,-1)
	r.goto(80,190,-1)
	
	#r.absrot()
	
		
	@_spawn
	def _():
		lfliper(2)
	rfliper(2)	
	

	r.goto(512,35) #Kupi pakove sa haosa 
	
	#r.goto(-716,-90)
	r.goto(860,-400)
	r.goto(1156, -520)
	
	
	r.forward(-300)
	
	
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)	
	

	return
	# OVO JE BILO VEC NAPISANO, NZM STA JE
	r.goto(800,-610,1) # red
	
	r.goto(200,-250,1)
	r.curve_rel(-310,120)
	r.goto(1100,-550,1)
	r.goto(1150,-550,1)'''
