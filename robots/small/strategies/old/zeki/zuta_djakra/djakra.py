weight=10
def run():
	#Inicijalizovanje svih pokretnih delova na robotu
	#zuta	
	r.speed(100)  	
	with disabled('collision'):
		r.curve_rel(-187, 145)	
	r.speed(220)
	   


	#r.goto(-935,-75add0,-1)
	r.goto(500,-300,1)
	r.speed(200)
	r.goto(-550,-300,1)#500
	
	#Otvaranje i zatvaranje pakova ide istovremeno i za levi i za desni
	
	
	rfliper(2)	
	r.speed(50)	
	r.curve_rel(-180,180)
	r.speed(230)
	r.absrot(-50)
	sleep(0.3)
	lfliper(2)
	r.absrot(0)

	
	
	r.speed(220)	
	r.goto(1156, -482)
	r.goto(1250,-482)
	r.absrot(0)
	
	r.forward(-200)
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)	
	#addpts(20)
	#izvuci se da ne smetas ananasu
	r.goto(850,-200,-1)
	
