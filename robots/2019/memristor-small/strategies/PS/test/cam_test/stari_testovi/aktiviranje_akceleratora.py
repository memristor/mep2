weight = 10
def run():

	# Pak za guranje 1300cm od ivice, 774
	# Pak za guranje: (200,1000)
	# Goldium: (726,1000)
	
      	
	r.speed(140) #bilo 180
	'''x,y = coord('gold_setpos')
	r.goto(x,y)
	r.absrot(-90)
	r.goto(x,y-200)
	r.speed(60)	
	
		
	def f():
		_goto(offset=1, ref='main')
	r.conf_set('enable_stuck', 1)
	_on('motion:stuck', f)
	r.absrot(-90)
	r.forward(150)
	r.setpos(y=-885)
	r.conf_set('enable_stuck', 0)

	r.speed(200) #bilo 180

	r.forward(-100)
	r.absrot(0)'''
	'''
	r.goto(0, 0)
	x,y= coord('aktiviranje_akceleratora')
	#r.goto(x,y,1)
	
	r.goto(x-100-10,y-25+14+5+7+5+6+3+50-20+150)

	
	@_do
	def _():
		print("tek sad ocitaj: ")
		atoms = cam_read()
		if len(atoms) == 1:
			a = atoms[0]
			r.turn(-90)
			r.forward(int(-a[1]) + 120)
			r.turn(90)
			r.forward(int(a[0]) - 140)
			r.turn(90)
			r.forward(300)


	r.goto(x-100-10,y-25-20+5+14+7+5+6+3+50-20+150, -1)
	r.goto(x,y-25+14+7+5+6-20+5+3,-1)
	r.absrot(180)
	lrucica(1)
	#r.forward(120)
	#r.goto(x+100,y,1)
	r.goto(x+100+20,y-25+14-15+7+5+6+3,-1)
	lrucica(0)
	#####
	# Nakon sto gurne pak 
	#Poeni za guranje plavog u akcelerator i otklj goldeniuma
	addpts(10)
	addpts(10)

	r.forward(-50)
	r.turn(8)
	'''
