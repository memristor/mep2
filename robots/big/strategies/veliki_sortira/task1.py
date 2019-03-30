
weight=2
def run():
	#r.setpos(1275,250,180) # green

	# odlazi do pakova i kupi 1, 2, 3
	r.speed(100)
	r.goto(1275,-370)  
	r.goto(875,-370)     # lokacija paka 2 [1025-(50+ i*100)]    i[0,5]
	sleep(1)

	# pre nego pokupi preostala dva paka treba da dobije informaciju od malog 
	# da li moze da ih skuplja 
	r.goto(200,-370) # ovde ide da izrotira
	r.absrot(0)
	r.goto(575,-370)  # lokacija paka 5  
	sleep(1)

	r.goto(250,-370,0) 
	r.goto(160,-390,0) # lokacija vage
	sleep(1)	
	r.absrot(0)
	sleep(1)
	# sortiranje pakova po poljima	
	
	# dolazak do polja 
	
	r.goto(250,-370,0)
	r.goto(800,-300,0)
	
	r.setpos(800,-300,0)
	#blue
	r.goto(800,-50,0)	
	r.absrot(0)
	
	r.goto(1250,-50,0)
	r.absrot(-45)
	sleep(1)
	
	#green
	r.goto(800,-50,0)
	r.goto(800,250,0)
	
	r.goto(1250,250,90)
	r.absrot(-45)
	sleep(1)

	# red 
	r.goto(800,250,0)
	r.goto(800,550,0)
	
	r.goto(1250,550,90)
	r.absrot(-45)	
	sleep(1)
	r.absrot(0)
	
