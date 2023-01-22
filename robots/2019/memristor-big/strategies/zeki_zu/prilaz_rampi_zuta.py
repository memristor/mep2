weight=15
def run():
		# r.goto(1500-155-125+200,1000-600-220+200,1)
		# sleep(50)
		r.speed(120)
		r.goto(1275,500,1) #pridji(udji) u rampu
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
		r.curve_rel(205,90)
		#r.absrot(10)
		#r.absrot(0)
		#r.speed(60)
		sleep(1)
		#PENJANJE GORE
		#-1080   810
		r.goto(350,810,1)
		#r.forward(720)
		pump(7,0)
		pump(8,0)
		pump(9,0)
		sleep(0.1)
		r.forward(-50)
		r.forward(95)
		rfliper(1)
		@_spawn
		def _():
			lfliper(1)
		sleep(2)
		rfliper(0)
		@_spawn
		def _():
			lfliper(0)	
		
		#precka stuck mozda upaliti NEMA POTREBE
		# r.conf_set('enable_stuck', 1)
		# _on('motion:stuck', f)
		# r.forward(200)
		# preska gotova cimni
		#r.conf_set('enable_stuck', 0)
		
		#SPUSTANJE DOLE
		r.speed(60) #brzina spustanja nizs rampu 60
		r.forward(-700) #spusti se niz rampu 680 bilo
		
		
		#RESETOVANJE x ---------------------------------------------
		r.conf_set('enable_stuck', 1) # reset x pozicije
		_on('motion:stuck', f)
		r.forward(-300)
		r.setpos(x=1500-225)
		r.conf_set('enable_stuck', 0)
		
		r.forward(200)# 200 izvuci se za kurvu
		sleep(7)
		r.speed(20) #20
		#r.absrot(0)
		r.curve_rel(205, -90) #izlaz iz prilaza
		
		r.absrot(90)
		#RESETOVANJE Y
		r.speed(50)#50
		r.conf_set('enable_stuck', 1) # reset y pozicije
		_on('motion:stuck', f)
		r.forward(500)
		r.setpos(y=1000-60)
		r.conf_set('enable_stuck', 0)
		#----------------------------------------------------------
		#r.goto(-1275,140,-1)
		
	
		#TEST KRAJ
		r.forward(-530)# izvlacenje
		r.forward(-200)
	
		return
