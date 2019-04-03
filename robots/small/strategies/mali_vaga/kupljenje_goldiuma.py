weight = 14
def run():

	# Pak za guranje 1300cm od ivice, 774
	# Pak za guranje: (200,1000)
	# Goldium: (726,1000)
	r.speed(150)
	r.goto(0,0,1)
	
	#r.goto(160,-860,1)
	r.goto(500, -600)
	r.absrot(-90)
	
	r.speed(50)	
		
	def  f():
		_goto(offset=1, ref='main')
	r.conf_set('enable_stuck', 1)
	_on('motion:stuck', f)
	r.goto(500,-1000)
	r.forward(200)
	r.setpos(y=-920)
	r.conf_set('enable_stuck', 0)
	#rrucica(1)
	r.forward(-100)
	r.absrot(0)
	r.goto(160,-860,-1)
	r.absrot(0)
	r.forward(100)

	#####
	# Nakon sto gurne pak 
	r.forward(-50)
	r.turn(10)
	r.forward(500)
	r.absrot(-90)

	# Implementirati stak umesto ovoga
	r.forward(120)
	r.forward(-100)	
