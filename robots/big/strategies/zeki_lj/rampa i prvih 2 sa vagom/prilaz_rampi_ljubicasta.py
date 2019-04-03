weight=15
def run():
		r.speed(120)
		r.forward(80) #odvoji se od zida
		r.goto(-1285,500,1) #pridji(udji) u rampu
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
		r.conf_set('enable_stuck', 0) # upali stuck
		r.forward(-340) # izvuci se za kurvu
		
		r.speed(60)#20
		r.forward(10)
		r.curve_rel(-205,90)
		#r.absrot(10)
		#r.absrot(0)
		#r.speed(60)
		sleep(1)
		#PENJANJE GORE
		#-1080   810
		r.goto(-350,810,1)
		#r.forward(720)
		pump(7,0)
		pump(8,0)
		pump(9,0)
		sleep(0.1)
		r.forward(-50)
		r.forward(95)
		@_spawn
		def _():
		
			rfliper(1)
			lfliper(1)
		sleep(2)
		@_spawn
		def _():
		
			rfliper(0)
			lfliper(0)	
		
		#precka stuck mozda upaliti
		# r.conf_set('enable_stuck', 1)
		# _on('motion:stuck', f)
		# r.forward(200)
		# preska gotova cimni
		#r.conf_set('enable_stuck', 0)
		
		#SPUSTANJE DOLE
		r.speed(60) #brzina spustanja nizs rampu 60
		r.forward(-680) #spusti se niz rampu
		sleep(1)
		
		#RESETOVANJE x ---------------------------------------------
		r.conf_set('enable_stuck', 1) # reset x pozicije
		_on('motion:stuck', f)
		r.forward(-300)
		r.setpos(x=-1500+225)
		r.conf_set('enable_stuck', 0)
		
		r.forward(200)# 200 izvuci se za kurvu
		sleep(2)
		r.speed(20) #20
		#r.absrot(0)
		r.curve_rel(-205, -90) #izlaz iz prilaza
		
		r.absrot(90)
		#RESETOVANJE Y
		r.speed(50)#50
		r.conf_set('enable_stuck', 1) # reset y pozicije
		_on('motion:stuck', f)
		r.forward(500)
		r.setpos(y=1000-65)
		r.conf_set('enable_stuck', 0)
		#---------------------------------------------------------------------
		r.forward(-530)# izvlacenje 
		r.curve_rel(-205,-70)   #NAMESTANJE ZA 123 sa kurvom  sa 90 prebacio
		sleep(2)
		return