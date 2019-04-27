weight=15
def run():
		#120 kurva
		#stuck 70
		_unlisten('collision')
		r.speed(250)
		r.goto(-1275,500,1) #pridji(udji) u rampu
		r.absrot(90)
		
		pump(7,1)
		pump(8,1)
		pump(9,1)
		
		r.speed(70) # brzina za nabijanje u pakove		mozda izbaciti 60
		def  f():
			_goto(offset=1, ref='main')
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f)
		r.forward(500)
		r.speed(150)#100
		r.conf_set('enable_stuck', 0) # upali stuck
		r.forward(-350) # izvuci se za kurvu 340 bilo
		r.speed(120)#80
		r.forward(10)
		r.curve_rel(-205,90)
		
		r.absrot(0)
		r.speed(110)
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
			lfliper(1)
		rfliper(1)
		@_spawn
		def _():
			lfliper(0)	
		rfliper(0)

		#SPUSTANJE DOLE
		r.speed(110) #brzina spustanja nizs rampu 80
		r.forward(-750) #spusti se niz rampu 700
		r.speed(120)
		#RESETOVANJE x ---------------------------------------------
		r.conf_set('enable_stuck', 1) # reset x pozicije
		_on('motion:stuck', f)
		r.forward(-300)
		r.setpos(x=-1500+225)
		r.conf_set('enable_stuck', 0)
		
		r.forward(200)# 200 izvuci se za kurvu
		r.speed(150) #60
		#r.absrot(0)
		r.curve_rel(-205, -90) #izlaz iz prilaza
		
		r.absrot(90)
		#RESETOVANJE Y
		r.speed(70)#50
		r.conf_set('enable_stuck', 1) # reset y pozicije
		_on('motion:stuck', f)
		r.forward(500)
		r.setpos(y=1000-60)
		r.conf_set('enable_stuck', 0)
		#----------------------------------------------------------
		#r.goto(-1275,140,-1)
		
		r.speed(180)
		#TEST KRAJ
		r.forward(-630)# izvlacenje530
		sleep(2)
		return
