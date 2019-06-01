weight = 3
def run():
	'''if State.pokupio == 0:
		pump(1,0)
		return'''
	r.goto(800,250)
	r.goto(800,-250,1)
	r.goto(1100,-250,-1) # da pak ispred polja da ne bi ovaj sa pumpe lupio u njega 
	#r.goto(1270,-550)
	#r.goto(1170,-550) # kada mali pogura pakove dalje ka zidu
	r.goto(1000,-250,1)
	r.turn(15)
	pump(1,0)
	
