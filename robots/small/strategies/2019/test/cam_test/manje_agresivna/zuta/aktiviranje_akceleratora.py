from core.Util import *
weight = 9
mali = _State(0, name='mali', shared=True)
def run():

	if State.goldenium_activated.val:
		return False
	# Pak za guranje 1300cm od ivice, 774
	# Pak za guranje: (200,1000)
	# Goldium: (726,1000)
	
	ents = _core.entities.get_entities_in_polygon(polygon_square_around_point([-680+100,-800], [300,50]))
	print('got ents', ents)
	if ents:
		return False
      
	
	r.speed(140) #bilo 180
	
	x,y=coord('aktiviranje_akceleratora')
	if not pathfind(x+128,y+62,-1): #tacka za koju treba odraditi pathfinding, ne sme na onu direktno kod zida
		return False
	r.goto(x,y+4,-1)
	r.absrot(0)
	rrucica(1)
	r.goto(x-120,y+4,-1)
	rrucica(0)
	State.goldenium_activated.val =1
	#####
	# Nakon sto gurne pak 
	#Poeni za guranje plavog u akcelerator i otklj goldeniuma
	addpts(10)
	addpts(10)

	#r.forward(22) 
	r.turn(-8)
	
def leave():
	rrucica(0)
