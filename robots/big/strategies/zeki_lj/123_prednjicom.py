weight=14
def run():
		r.speed(120)
		r.goto(-1100,360,-1) #izravnaj se dodati TOF NA OVOJ SU STRANI
		r.goto(-800,360,1) #izravnaj se dodati TOF NA OVOJ SU STRANI
		r.absrot(0)
		
		
		
		
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
		
		r.absrot(180)
		
		return
		
		
	
