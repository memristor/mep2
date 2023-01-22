weight=10
def run():
		#120 kurva
		#stuck 70
		_unlisten('collision')
		r.speed(50) ############################### smanjeno sa 200 na 50 zbog klizanja
		r.goto(1275-5-10,600+100+60+40+40+10+15+10,1) #pridji(udji) u rampu
		r.absrot(90)
		
		
		
		r.speed(20) # brzina za nabijanje u pakove		mozda izbaciti 60
		def  f():
			_goto(offset=1, ref='main')
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f)
		r.forward(500)
		r.speed(25)#100
		
		#####
		pump(7,1)
		sleep(0.04)
		pump(8,1)
		sleep(0.04)
		pump(9,1)
		sleep(0.04)
		
		sleep(0.04)
		pump(4,1)
		sleep(0.04)
		pump(5,1)
		sleep(0.04)
		pump(6,1)
		
		pump(7,1)
		sleep(0.04)
		pump(8,1)
		sleep(0.04)
		pump(9,1)
		sleep(0.04)
		#####
		
		r.conf_set('enable_stuck', 0) # ugasi stuck
		r.forward(-20)
		r.speed(50) ############################### smanjeno sa 150 na 50 zbog klizanja
		r.forward(-330) # izvuci se za kurvu 340 bilo
		r.speed(50)#80   ############################### smanjeno sa 80 na 50 zbog klizanja
		r.forward(10)
		r.curve_rel(205*2,90)
		sleep(0.1)
		r.absrot(180)
		r.speed(60)
		#PENJANJE GORE
		#-1080   810
		r.absrot(180)
		r.goto(350+30,780-5-10-3,1)
		
#		r.forward(700)
		_on('motion:stuck', f)
		r.conf_set('enable_stuck', 1)
		r.forward(200)
		r.conf_set('enable_stuck', 0)
		r.forward(-40)
		
		pump(7,0)
		pump(8,0)
		pump(9,0)
		
		sleep(0.04)
		pump(4,1)
		sleep(0.04)
		pump(5,1)
		sleep(0.04)
		pump(6,1)
		
		
		r.forward(-50)
		_on('motion:stuck', f, _name='ramp_stuck')
		r.conf_set('enable_stuck', 1)
		r.forward(95+30)
		_unlisten(_name='ramp_stuck')
		r.conf_set('enable_stuck', 0)
		r.forward(2)
		
		@_spawn
		def _():
			lfliper(1)
		rfliper(1)
		sleep(1)
		@_spawn
		def _():
			lfliper(0)	
		rfliper(0)
		
		addpts(32)
		
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
		r.speed(60) #brzina spustanja nizs rampu 80    ############################### smanjeno sa 80 na 50 zbog klizanja
		r.forward(-750) #spusti se niz rampu 700
		r.speed(30)
		#RESETOVANJE x ---------------------------------------------
		r.conf_set('enable_stuck', 1) # reset x pozicije
		_on('motion:stuck', f)
		r.forward(-300)
		r.setpos(x=1500-225)
		r.conf_set('enable_stuck', 0)
		
		r.speed(50)
		r.forward(200)# 200 izvuci se za kurvu
		r.speed(50) #60   ############################### smanjeno sa 100 na 50 zbog klizanja
		#r.absrot(0)
		sleep(0.1)
		r.curve_rel(205*2, -90) #izlaz iz prilaza
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
		
		r.speed(130) ############################### smanjeno sa 140 na 50 zbog klizanja
		r.forward(-700)# izvlacenje
		sleep(0.1)
		return
