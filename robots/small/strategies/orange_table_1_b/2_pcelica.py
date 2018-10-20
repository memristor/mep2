weight=10

def run():
	_unlisten('collision')
	r.speed(170) # dodato
	#  r.goto(-934,285) # r.goto(1200,430)
	if not pathfind(-934,285): # r.goto(1200,430)
		return False
		
	sleep(0.05)
	
	r.goto(-1297,687)
	#r.goto(-1297,800)
	r.turn(180)
	pcelica(2)
	r.goto(-1297,900,-1)
	pcelica(0)
	sleep(0.2) #plavi dodao
	#sleep(1) zakomentarisano
	r.forward(100)
	r.goto(-700,350)
	pcelica(0)


	#r.goto(-1269, 685) # r.goto(1600,95)
	#r.goto(-1269, 845) # r.goto(1760,95)
	#  r.turn(-90) ovo je bilo zakomnetarinao
	#pcelica(2)
	#r.goto(-1314, 845,1) # r.goto(1760,50,-1) sa 1314 na 1300j
	#pcelica(1)
	#r.goto(-1254, 845) # r.goto(1760,110)
	

def leave():
	pcelica(0)
