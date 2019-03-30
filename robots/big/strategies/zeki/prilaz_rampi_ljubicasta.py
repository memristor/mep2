weight=15
def run():
		r.speed(80)
		r.forward(80) #odvoji se od zida
		r.goto(-1325,500,1) #pridji(udji) u rampu
		r.absrot(90)
		
		pump(7,1)
		pump(8,1)
		pump(9,1)

		r.speed(50) # brzina za nabijanje u pakove		mozda izbaciti
		def  f():
			_goto(offset=1, ref='main')
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f)
		r.forward(500)
		
		r.forward(-340) # izvuci se za kurvu
		r.conf_set('enable_stuck', 0) # upali stuck
		r.speed(20)
		r.forward(10)
		r.curve_rel(-205,90)
		r.absrot(0)
		r.speed(60)
		sleep(0.1)
		#PENJANJE GORE
		r.forward(720)
		pump(7,0)
		pump(8,0)
		pump(9,0)
		sleep(0.1)
		r.forward(-50)
		sleep(0.1)
		#precka stuck mozda upaliti
		# r.conf_set('enable_stuck', 1)
		# _on('motion:stuck', f)
		# r.forward(200)
		# preska gotova cimni
		#r.conf_set('enable_stuck', 0)
		
		#SPUSTANJE DOLE
		r.speed(60) #brzina spustanja nizs rampu
		r.forward(-680) #spusti se niz rampu
		sleep(3)
		
		#RESETOVANJE x ---------------------------------------------
		r.conf_set('enable_stuck', 1) # reset x pozicije
		_on('motion:stuck', f)
		r.forward(-500)
		r.setpos(x=-1278)
		r.conf_set('enable_stuck', 0)
		
		r.forward(175)# 200 izvuci se za kurvu
		r.speed(20)
		r.absrot(0)
		r.curve_rel(-205, -90) #izlaz iz prilaza
		
		#RESETOVANJE Y
		r.speed(50)
		r.conf_set('enable_stuck', 1) # reset y pozicije
		_on('motion:stuck', f)
		r.forward(500)
		r.setpos(y=-940)
		r.conf_set('enable_stuck', 0)
		#---------------------------------------------------------------------
		
		r.forward(-450)# izvlacenje bilo 455
		r.curve_rel(205,90)   #NAMESTANJE ZA 123 sa kurvom PROVERI da li ide minus
		sleep(2)
		#izvukao sam se iz rampe i imam resetovano x i y
		
		
		
		#KUPLJENJE 1,2,3  DESNOM STRANOMdodaj tacno pozicioniranje za 123
		r.goto(-930,330,1) #izravnaj se dodati TOF NA OVOJ SU STRANI
		pump(4,1)
		pump(5,1)
		pump(6,1)
		#desnilift(0)
		sleep(2)
		rlift(2)
		sleep(1)
		rlift(1)
		#desnilift(1)
		
		r.goto(-760,-340,-1) #IDI DO 123  bilo 300
		r.absrot(0)
		r.goto(-510,355,1)# pridji 456
		#KUPLJENJE 4,5,6
		pump(1,1)
		pump(2,1)
		pump(3,1)
		#levilift(0)
		sleep(2)
		llift(2)
		sleep(1)
		llift(1)
		#levilift(1)
		
		
		
		
		
		
		#-------------------------------------
		sleep(3) # ugasi sve
		pump(8,0)
		pump(9,0)
		pump(7,0)
		pump(1,0)
		pump(2,0)
		pump(3,0)
		return
		