#weight = 3
#def run():

weight = 1
def run():

	r.speed(150)	
	r.forward(-330)
			
	

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
	addpts(7)

	r.speed(100)
	r.goto(-1000+10+160,-500-20-5-55,1)
	r.absrot(180)
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




	
