weight=15
def run():
		
		r.speed(80)
		r.goto(-1275,500,1) #pridji(udji) u rampu
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
		r.speed(100)
		r.conf_set('enable_stuck', 0) # upali stuck
		sleep(6)
		r.forward(-340) # izvuci se za kurvu
		
		
		
		r.speed(80)
		#TEST KRAJ
		
		sleep(2)
		r.goto(-1275,-150,-1)
		pump(7,0)
		pump(8,0)
		pump(9,0)
		return
