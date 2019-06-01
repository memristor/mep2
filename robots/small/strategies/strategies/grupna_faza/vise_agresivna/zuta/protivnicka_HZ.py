weight=99
def run():
	#Inicijalizovanje svih pokretnih delova na robotu
	r.goto(-550,-340,1)#500
	r.absrot(180)

	
	@_spawn
	def _():
		rfliper(2)
	lfliper(2)	
	r.speed(50)	
	r.curve_rel(-180,180)
	r.absrot(0)	
	r.speed(180)
	r.goto(1156,-517)
	r.goto(1250,-517)
	r.absrot(0)
	
	r.forward(-200)
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)	
	addpts(14) # 2 crvena su na svojim mestima (2x6) i plavi i zeleni (2x1) 
	r.speed(180)
	
