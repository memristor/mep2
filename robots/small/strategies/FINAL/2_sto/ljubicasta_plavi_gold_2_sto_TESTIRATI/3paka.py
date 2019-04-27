#weight = 3
#def run():

weight = 1
def run():

	r.speed(200)	
	r.forward(-400)
			
	

	#Odavde ubaciti Dusanovo
	
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)

	r.goto(-1000,275,-1)

	@_spawn
	def _():
		lfliper(2)
	rfliper(0)

	#Jos jedan bod za ubacivanje poslednjeg paka
	

	r.speed(100)
	r.goto(-950,-500-90,1)
	r.absrot(180)
	addpts(7)
	r.forward(150)
	r.forward(-150)
	
	return

	'''### DUSAN Ubaciti ovo i probati	
	lfliper(2)
	r.goto(1000, 50-50)
	r.goto(1050, 50-50)
	lfliper(1)

	r.goto(1000, -400)
	
	r.goto(1170,-450)

	lfliper(2)

	r.forward(-100)
	lfliper(0)'''




	
