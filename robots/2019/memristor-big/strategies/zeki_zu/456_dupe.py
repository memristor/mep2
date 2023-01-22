weight=13
def run():
		
		r.goto(-700,360,-1)# pridji 365 inicijalno 360
		r.absrot(180)

		#KUPLJENJE 4,5,6
		lift(1,'sredina')  #skuplja goldenium
		@_spawn
		def _():
			pump(4,1)
			pump(5,1)
			pump(6,1)
		
		rlift(2)
		sleep(2)
		rlift(1)
		#lift(1,'pri_vrhu',1) # podize malo da se pak moze izvuci 
		lift(1,'sredina',1)
		
		r.goto(-900,350,1)# pridji 365 inicijalno 360
		r.goto(-1200,300,1)# pridji 365 inicijalno 360
		return
		
		
		
		