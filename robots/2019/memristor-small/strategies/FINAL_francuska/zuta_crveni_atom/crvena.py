weight = 9
def run():
	
	#Pozicija zelenog 1-ispred rediuma, 2-ispred grinijuma, 3-ispred blumiuma
	poz_crv = 3
	 

	r.speed(50)
	r.curve_rel(200, -140)	
	r.speed(180)
	r.goto(200,0, -1) # Da krene ka periodnom sistemu sa centra
	
	if (poz_crv == 1):
		rfliper(2)		
		r.goto(1000, -500+50) #+50 toliko pomera da upadne u levi fliper
		r.goto(1050, -500+50)
		rfliper(1)
	elif (poz_crv == 2):
		rfliper(2)
		r.goto(1000, -250-50)
		r.goto(1050,-250-50 )
		rfliper(1)
	else:
		lfliper(2)
		r.goto(1000, 50-50)
		r.goto(1050, 50-50)
		lfliper(1)
		r.goto(1000, -400)
	
	r.goto(1170,-450) #Pozicija ostavljanja 

	if(poz_zel == 3):
		lfliper(2)
	else: 
		rfliper(2)
	r.forward(-200)
	lfliper(0)
	rfliprer(0)

	addpts(6)

	'''
	r.goto(-800,-250,1)
	r.goto(-1100,-250,-1) # da pak ispred polja da ne bi ovaj sa pumpe lupio u njega 
	#r.goto(-1270,-250)
	#r.goto(-1170,-250) # kada mali pogura pakove dalje ka zidu
	r.goto(-1000,-250,1)
	r.turn(15)
	pump(1,0)'''

	 
	