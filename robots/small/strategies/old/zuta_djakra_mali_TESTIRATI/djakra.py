weight=2
def run():
	#Inicijalizovanje svih pokretnih delova na robotu
		
	   	
	r.speed(50)
	r.curve_rel(-180, 145)#bilo 200 	
	r.speed(140)
	   


	#r.goto(-935,-750,-1)
	r.goto(500,-300,1)
	r.goto(-550,-300,1)#500
	
	#Otvaranje i zatvaranje pakova ide istovremeno i za levi i za desni
	
	
	rfliper(2)	
	r.speed(50)	
	r.curve_rel(-180,180)
	r.speed(230)
	r.absrot(230)
	sleep(2)
	lfliper(2)
	r.absrot(0)
		
	#r.goto(790,290,-1)
	
	#Otvaranje i zatvaranje pakova ide istovremeno i za levi i za desni
	#@_spawn
	#def _():
	#    rfliper(2)
	#lfliper(2)
	#r.forward(520)
	#@_spawn
	#def _():
	#    rfliper(1)
	#lfliper(1)
	#r.absrot()
	
	#r.goto(257,-110)
	#r.goto(-716,-90)
	r.speed(240)	
	r.goto(1156, -482)
	r.goto(1250,-482)
	r.absrot(180)
	
	r.forward(200)
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)	
	#addpts(20)
	#izvuci se da ne smetas ananasu
	r.goto(400,-200)
	
	#addpts(14) # 2 crvena su na svojim mestima (2x6) i plavi i zeleni (2x1) 
	#na kraju zatvori flipere
