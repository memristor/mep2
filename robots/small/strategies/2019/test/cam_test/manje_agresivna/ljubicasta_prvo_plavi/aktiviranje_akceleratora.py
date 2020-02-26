from core.Util import *
weight = 8
def run():

	if State.goldenium_activated.val:
		return False
	# Pak za guranje 1300cm od ivice, 774
	# Pak za guranje: (200,1000)
	# Goldium: (726,1000)
	
	ents = _core.entities.get_entities_in_polygon(polygon_square_around_point([680-100,-800], [300,50]))
	print('got ents', ents)
	if ents:
		return False
	
      	
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

	x,y= coord('aktiviranje_akceleratora')
	#r.goto(x,y,1)
	# r.goto(x-100,y-25+14+7+5+6+3+50-2,-1) #tacka za koju treba odraditi pathfinding, ne sme na onu direktno kod zida
	if not pathfind(x-100-10,y-25+14+7+5+6+3+50-2+40-20-10,-1): #tacka za koju treba odraditi pathfinding, ne sme na onu direktno kod zida
		return False
	r.goto(x,y-25+14+7+5+6+3-1-1,-1)
	r.absrot(180)
	lrucica(1)
	#r.forward(120)
	#r.goto(x+100,y,1)
	r.goto(x+100+20,y-25+14+7+5+6+3-1-1,-1)
	lrucica(0)
	State.goldenium_activated.val =1
	addpts(10)
	addpts(10)
	#####
	# Nakon sto gurne pak 
	#Poeni za guranje plavog u akcelerator i otklj goldeniuma

	r.forward(-50)
	r.turn(7)

def leave():
	lrucica(0)
