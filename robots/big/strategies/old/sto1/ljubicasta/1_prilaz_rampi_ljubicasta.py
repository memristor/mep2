weight=15
def run():
		_unlisten('collision')
		r.speed(120)
		# r.forward(-60)
		# r.goto(1265,500,1) #pridji(udji) u rampu
		r.goto(*coord('prilaz_rampi'),1) #pridji(udji) u rampu
		r.absrot(90)
		
		for i in (7,8,9):	
			pump(i,1)
			
		r.speed(50) # brzina za nabijanje u pakove		mozda izbaciti
		
		def  f():
			_goto(offset=1, ref='main')
		
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f)
		
		r.forward(500)
		r.conf_set('enable_stuck', 0) # upali stuck
		
		r.forward(-340) # izvuci se za kurvu
		
		r.speed(80)#20
		r.forward(10)
		r.curve_rel(-205,90)
		
		sleep(0.1)
		r.absrot(0)
		r.speed(40)

		r.conf_set('enable_stuck', 1) 
		_on('motion:stuck', f)
		r.forward(-500)
		r.setpos(x=-1500+225,o=0)
		r.conf_set('enable_stuck', 0)
		
		# penjanje na rampu
		r.speed(50)#bilo 70
		#r.goto(-350,800,1)# PAZI OVO SAD 800
		r.forward(900)
		
		p1 = [pressure(i) for i in (7,8,9)]
		
		@_do
		def _():
			State.pumpe[7].val = 'crveni' if p1[0].val else False
			State.pumpe[9].val = 'zeleni' if p1[1].val else False
			State.pumpe[8].val = 'plavi' if p1[2].val else False
		
		for i in (7,8,9):	
			pump(i,0)
			
		sleep(1.5)
		
		p2 = [pressure(i) for i in (7,8,9)]
		
		
		@_do
		def _():
			for i in (7,8,9):
				if State.pumpe[i].val != False and p2[i-7].val == False:
					addpts(State.color_vaga_bodovi[State.pumpe[i].val])
					State.pumpe[i].val = False
			addpts(State.color_vaga_bodovi['zeleni'])
			
		
		r.forward(-50)
		r.forward(95)
		
		
		with _parallel():
			lfliper(1)
			rfliper(1)
		
		_sync()
		
		with _parallel():
			lfliper(0)
			rfliper(0)
		
		
		#SPUSTANJE DOLE
		r.speed(60) #brzina spustanja nizs rampu 60
		r.forward(-750) #spusti se niz rampu 680 bilo
		
		r.speed(50)
		#RESETOVANJE x ---------------------------------------------
		r.conf_set('enable_stuck', 1) # reset x pozicije
		_on('motion:stuck', f)
		r.forward(-300)
		r.setpos(x=-1500+225, o=0)
		r.conf_set('enable_stuck', 0)
		
		r.forward(200)# 200 izvuci se za kurvu
		r.speed(100) #20
		#r.absrot(0)
		r.curve_rel(-205, -90) #izlaz iz prilaza
		
		r.absrot(90)
		
		#RESETOVANJE Y
		r.speed(50)#50
		r.conf_set('enable_stuck', 1) # reset y pozicije
		_on('motion:stuck', f)
		r.forward(500)
		r.setpos(y=1000-60, o=90)
		r.conf_set('enable_stuck', 0)
		#----------------------------------------------------------
		
		r.speed(100)
		r.forward(-30)# izvlacenje
		with _parallel():
			llift(0)
			rlift(0)
			lift(2,'sredina')
			lift(1,'sredina')
		r.goto(-1230+20,200,-1)
		_sync()
		sleep(0.1)

