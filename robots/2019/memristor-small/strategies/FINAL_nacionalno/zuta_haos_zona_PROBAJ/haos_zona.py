weight = 3
def run():

	# Pak za guranje 1300cm od ivice, 774
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
	r.goto(-1195,-775,-1)
	r.absrot(-180)
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
	r.goto(1150,-550,1)
