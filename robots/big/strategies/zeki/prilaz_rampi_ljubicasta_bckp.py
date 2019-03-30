#weight=15
def run():
		r.speed(80)
		
		r.forward(80)
		r.goto(-1325,500,1) #ulaz u rampu
		r.absrot(90)
		
		pump(7,1)
		pump(8,1)
		pump(9,1)

		r.speed(50) # brzina za nabijanje u pakove		
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
		
		r.forward(720)
		pump(7,0)
		pump(8,0)
		pump(9,0)
		sleep(0.1)
		r.forward(-50)
		sleep(0.1)
		#precka stuck
		# r.conf_set('enable_stuck', 1)
		# _on('motion:stuck', f)
		# r.forward(200)
		# preska gotova cimni
		r.conf_set('enable_stuck', 0)
		
		r.speed(60) #40 slabo
		r.forward(-680) #spusti se niz rampu
		sleep(3)
		
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f)
		r.forward(-500)
		r.setpos(x=-1278)
		r.conf_set('enable_stuck', 0)
		r.forward(175)# 200

		
		sleep(1)
		r.speed(20)
		r.absrot(0)
		r.curve_rel(-205, -90) #izlaz iz prilaza
		r.speed(50)
		r.forward(-450)# izvlacenje bilo 455
		
		
		r.curve_rel(-205,90)
		sleep(2)
		
		
		
		
		# NOOOOOOOOOOOOOOVOO
		pump(1,1)
		pump(2,1)
		pump(3,1)
		r.forward(240)
		sleep(4)
		r.forward(420)
		#r.absrot(90)
		r.curve_rel(-205, -90)
		r.absrot(90)
		
		
		r.speed(50) # brzina za nabijanje u pakove		
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f)
		r.forward(500)
		r.forward(-340) # izvuci se 
		r.conf_set('enable_stuck', 0) # upali stuck
		
		sleep(3)
		pump(8,0)
		pump(9,0)
		pump(7,0)
		pump(1,0)
		pump(2,0)
		pump(3,0)
		