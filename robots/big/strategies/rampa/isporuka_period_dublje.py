weight=11
def run():
		#-----------------------------------------------------------------------------
		#isporuka plavog
		r.speed(100)
		r.goto(-1180,110,1)  
		r.absrot(-90)
		pump(4,0)
		sleep(1)
		
		#isporuka zeleni prvi
		r.goto(-1180,-390,1) 
		pump(5,0) # zeleni
		
		#isporuka crveni
		r.goto(-1180,-520,1)  #bilo 600
		pump(6,0)
		
		# OKRETANJE
		r.goto(-1180,-620,1) 
		r.absrot(90)
		#crveni drugi put
		r.goto(-1180,-570,1) 
		pump(3,0)
		
		#zeleni drugi put i crveni
		r.goto(-1180,-290,1)  
		pump(1,0) # crveni drugi
		
		r.goto(-1180,-270,1) 
		pump(2,0) # zeleni drugi
		sleep(1)
		return
		#dodati spustanje lifta skroz dole
		
