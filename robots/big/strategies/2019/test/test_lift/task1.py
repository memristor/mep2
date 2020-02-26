
weight= 4
def run():
	lift(1,'dole', 0)
	lift(2,'dole', 0)
	return
	#lift_drv.conf_set('speed2',100) #setovanje brzine lift br. 2
	lift(2,'goldenium')  #skuplja goldenium
	lift(2,'goldenium',1)	#odize malo da se goldenijum moze izvuci
	lift(2,'accel')  #postavlja pakove na akcelerator
	lift(2,'accel',1) # odize malo da pakovi ne dodoiruju zidove(treba testirati)
	lift(2,'pri_vrhu') # hvata bocne pakove pri vrhu(ih uhvati)
	lift(2,'pri_vrhu',1) # podize malo da se pak moze izvuci  
	lift(2,'sredina') #hvata bocne pakove po njihovoj sredini
	lift(2,'sredina',1) # podize malo da se pak moze izvuci 
	
	#lift_drv.conf_set('speed1',80)
	lift(1,'goldenium')
	lift(1,'goldenium',1)	
	lift(1,'accel')
	lift(1,'accel',1)
	lift(1,'pri_vrhu')
	lift(1,'pri_vrhu',1)
	lift(1,'sredina')
	lift(1,'sredina',1)
	
	
	#rad u paraleli
	'''
	
	@_spawn
	def _():
		lift(2,'goldenium')  #skuplja goldenium
		lift(2,'goldenium',1)	#odize malo da se goldenijum moze izvuci			
		lift(2,'accel')  #postavlja pakove na akcelerator
		lift(2,'accel',1) # odize malo da pakovi ne dodoiruju zidove(treba testirati)
		lift(2,'pri_vrhu') # hvata bocne pakove pri vrhu(ih uhvati)
		lift(2,'pri_vrhu',1) # podize malo da se pak moze izvuci  		
		lift(2,'sredina') #hvata bocne pakove po njihovoj sredini		
		lift(2,'sredina',1) # podize malo da se pak moze izvuci 
	
	
	@_spawn	
	def _():
		lift(1,'sredina')
		lift(1,'sredina',1)
		lift(1,'goldenium')
		lift(1,'goldenium',1)
		lift(1,'pri_vrhu')
		lift(1,'pri_vrhu',1)	
		lift(1,'accel')
		lift(1,'accel',1)
		
		
	
	sleep(500) # mora sleep da se main ne bi zavrsio , jer spawn napravi dva treda koji rade paralelno s mainom +
	'''
