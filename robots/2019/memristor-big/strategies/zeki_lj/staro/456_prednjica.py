#weight=10
def run():
		r.speed(150)
		r.forward(130)
		
		r.goto(-640,300,1) #pridji 4,5,6
		r.absrot(90) #ispravi se
		
		
		pump(7,1) #pali pumpe
		pump(8,1)
		pump(9,1)
		
		
		def  f():
			_goto(offset=1, ref='main')
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f)
		
		r.speed(50) #uspori
		r.forward(200) #zakucaj se

		
		#r.setpos(y=470)   # nakon nabijanja
		r.forward(-300)
		r.conf_set('enable_stuck', 0)
		r.speed(130) #ubrzaj se
		
		#-----------------------------------------------------------------------------
		#isporuka plavog
		r.goto(-1050,100,1)  # prednjica ako je 1
		r.absrot(180)
		pump(7,0)
		sleep(1)
		r.forward(-200)
		
		#isporuka zeleni
		#r.absrot(-90)
		r.goto(-1050,-350,1)  # prednjica ako je 1
		r.absrot(180)
		pump(8,0)
		sleep(1)
		r.forward(-200)
		
		#isporuka crveni
		#r.absrot(-90)
		r.goto(-1050,-550,1)  # prednjica ako je 1
		r.absrot(180)
		pump(9,0)
		sleep(1)
		r.forward(-200)
		
