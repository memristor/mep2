weight=13
def run():
		
		r.goto(-485,370,1)# pridji 365 inicijalno
		r.absrot(0)

		#KUPLJENJE 4,5,6
		lift(2,'sredina')  #skuplja goldenium
		@_spawn
		def _():
			pump(1,1)
			pump(2,1)
			pump(3,1)
		
		llift(2)
		sleep(2)
		llift(1)
		#lift(1,'pri_vrhu',1) # podize malo da se pak moze izvuci 
		lift(2,'sredina',1)
		
		#----------------------------------------
		
		#isporuka plavog
		r.goto(-1050,100,-1)  # prednjica ako je 1
		r.absrot(180)
		pump(7,0)
		sleep(1)
		r.forward(-200)
		
		
		
		return
		
		
		
		