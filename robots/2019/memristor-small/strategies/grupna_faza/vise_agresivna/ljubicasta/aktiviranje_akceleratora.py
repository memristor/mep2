from core.Util import *
weight = 9
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
	

	x,y= coord('aktiviranje_akceleratora')
	#r.goto(x,y,1)
	# r.goto(x-100,y-25+14+7+5+6+3+50-2,-1) #tacka za koju treba odraditi pathfinding, ne sme na onu direktno kod zida
	if not pathfind(x-133,y-59,-1): #tacka za koju treba odraditi pathfinding, ne sme na onu direktno kod zida
		return False
	r.goto(x,y-4,-1)
	r.absrot(180)
	lrucica(1)
	#r.forward(120)
	#r.goto(x+100,y,1)
	r.goto(x+100+20,y-4,-1)
	lrucica(0)
	State.goldenium_activated.val =1
	addpts(10)
	addpts(10)
	#####
	# Nakon sto gurne pak 
	#Poeni za guranje plavog u akcelerator i otklj goldeniuma

	
	r.turn(8)

def leave():
	lrucica(0)
