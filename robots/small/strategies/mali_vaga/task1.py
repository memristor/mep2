weight=15 #mali_kupi_plavi_za_vagu na malom
def run():

	#koordinate plavog paka (-697, 554)
	r.speed(150)
	nazgold(0)
	r.forward(-100)

	#Mora da zaobidje prvi pak ispred pocetne pozicije
	r.turn(-60)
	r.curve_rel(-380, -110)
	r.curve_rel(-300, -100)
	
	r.goto(-800,260,-1)
	r.goto(-715,395,-1)
	r.absrot(-90)
	pump(1,1)
	nazgold(2)
	r.forward(-15)
	sleep(2)
	r.speed(80)
	r.forward(200)
	nazgold(0)

	return	#Uzeo je plavi pak
	
	#r.goto(-800,-200) #Uzimam pak ispred grinijuma i stavljam u desni pak
	r.turn(-135)	
	
	r.goto(-1050,-220) 

	r.goto(-1000,-550) #Kupim drugi pak
	
	#Ako je jedan od dva paka crvene boje
	r.goto(-1350,-550)
	r.forward(-50)
	r.absrot(90)
	# Otvaram fliper gde je crveni pak
	r.goto(-1300,-300) #Idem na zeleno polje
	# Ako jeste zeleni pak onda: r.turn(90) r.forward(50) r.forward(-50) r.turn(-90)
	#Pustam crveni pak koji mu je na dupetu
	r.goto(-1300,0) #Idem na plavo polje, da ostavim ako je neki pak bio plave boje
	
	#Posle odavde treba da ide na sledeci task

	# Sluacaj kada nije uhvacen crveni pak
	#r.absrot(-30)	#Rotiram se da bih ostavio pak sa pumpe
	#r.forward(-50)
	
	return
	sleep(1) # Da pokupi pak vakuum pumpom
	r.forward(-100)

	
	r.goto(-1000,540)

