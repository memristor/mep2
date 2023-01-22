weight=14
def run():
		# r.forward(-450)# izvlacenje 
		# r.curve_rel(-205,-70)   #NAMESTANJE ZA 123 sa kurvom  sa 90 prebacio
		# sleep(2)
		llift(1)
		r.speed(80)
		#izvukao sam se iz rampe i imam resetovano x i y
		r.forward(-100)
		
		#KUPLJENJE 1,2,3  DESNOM STRANOMdodaj tacno pozicioniranje za 123
		r.goto(-995,365,-1) #izravnaj se dodati TOF NA OVOJ SU STRANI
		r.absrot(180)
		
		
		
		
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
		r.goto(-760,300,-1) #odvoji se od 123
		r.absrot(0)
		
		return
		
		
	