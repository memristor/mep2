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

	r.goto(1000,275,-1)

	@_spawn
	def _():
		lfliper(0)
	rfliper(2)

	r.goto(900,-500,1)
	r.absrot(0)
	addpts(7)
	r.forward(50)
	r.forward(-50)
	
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




	