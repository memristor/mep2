#weight=10
#ubacivanje u vagu 
def run():
		#MORA PREDNJICOMDA PRILAZI
		pump(1,1) #pali pumpe
		pump(2,1)
		pump(3,1)
		sleep(3)
		r.speed(150)
		r.forward(75)
		#r.absrot(90)
		r.goto(-1250,350,1) #pridji 4,5,6
		r.absrot(0) #ispravi se
		r.goto(-930,330,1) #IDI DO 123  bilo 300
		sleep(2)
		r.goto(-105,410,1) #IDI DO 4,5,6
		
		r.absrot(0)
		
		return
		
		def  f():
			_goto(offset=1, ref='main')
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f)
		
		r.speed(50) #uspori
		r.forward(190) #zakucaj se

		
		#r.setpos(y=470)   # nakon nabijanja
		r.forward(-300)
		r.conf_set('enable_stuck', 0)
		r.speed(130) #ubrzaj se
		
		#-----------------------------------------------------------------------------
		