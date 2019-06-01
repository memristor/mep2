weight = 3
def run():

	# Pak za guranje 1300cm od ivice, 774
	# Pak za guranje: (200,1000)
	# Goldium: (726,1000)
	

	
	r.curve_rel(-180, -140)
	r.speed(120)

	
	#r.goto(-140,-775,-1)
	r.goto(-80,190,-1)
	
	#r.absrot()
	
		
	@_spawn
	def _():
		lfliper(2)
	rfliper(2)	
	

	r.goto(-512,35)		# Valjalo bi da se uradi sa dva kretanja da bi pokupio sve pakove
	#r.goto(-350, 172)
	#r.goto(-600, -78) 
	
	#r.goto(-716,-90)
	r.goto(-860,-550)
	#r.goto(-1000, -550) 
	r.goto(-1100,-550) #r.goto(-1270,-550)
	
	r.forward(-300)
	
	
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)	
	
	
	return
	
