weight=11
def run():
		#-----------------------------------------------------------------------------
		#isporuka plavog
		r.goto(-1220,130,-1)  # prednjica ako je 1
		r.absrot(-90)
		pump(1,0)
		sleep(1)
		
		r.goto(-1220,-350,-1)  # prednjica ako je 1
		pump(3,0)
		
		#isporuka zeleni
		#r.absrot(-90)
		r.goto(-1100,-350,1)  # prednjica ako je 1
		
		r.goto(-1220,-350,1)  # prednjica ako je 1
		pump(6,0)#zeleni

		sleep(1)
		
		
		#isporuka crveni
		#r.absrot(-90)
		r.goto(-1200,-600,1)  # prednjica ako je 1
		
		pump(2,0)
		pump(5,0)
		pump(4,0)
		sleep(1)
	
		
