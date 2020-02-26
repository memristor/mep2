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
	if not pathfind(x-110-5+5,y+68+5,-1): #tacka za koju treba odraditi pathfinding, ne sme na onu direktno kod zida
		return False
		
	if State.must_stuck.val:
		r.absrot(-90)
		r.speed(40)
		# r.setpos(y=-885)
		r.stuckpos(1, y=-885-5+4)
		r.speed(140)
		r.forward(-100)
	
	r.goto(x,y+3+2+2+2+3-3,-1)
	r.absrot(180)
	lrucica(1)
	#r.forward(120)
	#r.goto(x+100,y,1)
	r.goto(x+120,y+3+2+2+2+3-3,-1)
	lrucica(0)
	State.goldenium_activated.val = 1
	addpts(10)
	addpts(10)
	#####
	# Nakon sto gurne pak 
	#Poeni za guranje plavog u akcelerator i otklj goldeniuma

	r.forward(+120)
	r.turn(6)
	r.forward(-50)#dodao macak 

def leave():
	lrucica(0)
