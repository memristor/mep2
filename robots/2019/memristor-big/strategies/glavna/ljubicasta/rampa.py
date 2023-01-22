weight=10
def run():
		# sleep(1)
		#120 kurva
		#stuck 70
		_unlisten('collision')
		r.speed(130)
		r.goto(-1275-8-7-2,600+100+60+40+40+10+15+10,1) #pridji(udji) u rampu
		r.absrot(90)
		
		pump(7,1)
		pump(8,1)
		pump(9,1)
		
		
		#####
		# pump(7,1)
		# sleep(0.04)
		# pump(8,1)
		# sleep(0.04)
		# pump(9,1)
		# sleep(0.04)
		
		# sleep(0.04)
		# pump(4,1)
		# sleep(0.04)
		# pump(5,1)
		# sleep(0.04)
		# pump(6,1)
		
		# pump(7,1)
		# sleep(0.04)
		# pump(8,1)
		# sleep(0.04)
		# pump(9,1)
		# sleep(0.04)
		#####
		
		r.speed(20) # brzina za nabijanje u pakove		mozda izbaciti 60
		def  f():
			_goto(offset=1, ref='main')
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f)
		r.forward(500)
		r.speed(25)#100
		r.conf_set('enable_stuck', 0) # iskljuci stuck
		r.forward(-20)
		r.speed(130)
		r.forward(-330) # izvuci se za kurvu 340 bilo
		r.speed(60)#80
		r.forward(10)
		r.curve_rel(-205,90)
		sleep(0.1)
		r.absrot(0)
		#r.speed(60)
		#PENJANJE GORE
		#-1080   810
		#r.forward(270)
		#@_spawn
		#def _():
		#	lfliper(1)
		#rfliper(1)
		
		# if get stuck
		
		######
		def g():
			_goto('ramp_stuck', ref='main')
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f, _name='ramp_stuck')
		######
		
		r.goto(-350-30,810-5-5-2,1)
		r.forward(40)
		pump(7,0)
		sleep(0.1)
		pump(6,1)
		
		sleep(0.4)
		
		pump(8,0)
		sleep(0.1)
		pump(5,1)
		
		sleep(0.4)
		
		pump(9,0)
		sleep(0.1)
		pump(4,1)
		
		sleep(0.4)
		
		r.forward(-50)
		r.forward(95+20+30-40)
		#####
		_L('ramp_stuck')
		r.conf_set('enable_stuck', 0)
		_unlisten(_name='ramp_stuck')
		r.forward(0)
		######
		
		
		
		
		@_spawn
		def _():
			lfliper(1)
		rfliper(1)
		@_spawn
		def _():
			lfliper(0)	
		rfliper(0)
		
		addpts(28)
		
		'''@_do
		def _():
			State.pumpe[7].val = 'plavi' if p1[0].val else False
			State.pumpe[9].val = 'zeleni' if p1[1].val else False
			State.pumpe[8].val = 'crveni' if p1[2].val else False
			
		p2 = [pressure(i) for i in (7,8,9)]
		
		@_do
		def _():
			for i in (7,8,9):
				if State.pumpe[i].val != False and p2[i-7].val == False:
					addpts(State.color_vaga_bodovi[State.pumpe[i].val])
					State.pumpe[i].val = False
			addpts(State.color_vaga_bodovi['zeleni'])
		'''
			

		#SPUSTANJE DOLE
		r.speed(80) #brzina spustanja nizs rampu 80
		r.forward(-750) #spusti se niz rampu 700
		r.speed(50)
		#RESETOVANJE x ---------------------------------------------
		r.conf_set('enable_stuck', 1) # reset x pozicije
		_on('motion:stuck', f)
		r.forward(-300)
		r.setpos(x=-1500+225)
		r.conf_set('enable_stuck', 0)
		
		'''#Kupi onaj crveni sto je ostao:
		r.forward(20)
		r.absrot(5)
		r.forward(100)
		r.absrot(0)
		llift(2)
		pump'''
		
		
		r.forward(200)# 200 izvuci se za kurvu
		r.speed(100) #60
		#r.absrot(0)
		sleep(0.1)
		r.speed(60)
		r.curve_rel(-205, -90) #izlaz iz prilaza
		sleep(0.1)
		r.absrot(90)
		#RESETOVANJE Y
		r.speed(50)
		r.conf_set('enable_stuck', 1) # reset y pozicije
		_on('motion:stuck', f)
		r.forward(500)
		r.setpos(y=1000-60)
		r.conf_set('enable_stuck', 0)
		#----------------------------------------------------------
		#r.goto(-1275,140,-1)
		
		#pump(8,1)
		#sleep(0.1)
		r.speed(130)
#with _parallel():
			#llift(0)
			#rlift(0)
			#lift(2,'sredina')
			#lift(1,'sredina')
		r.forward(-620)# izvlacenje
		sleep(0.1)
		return
