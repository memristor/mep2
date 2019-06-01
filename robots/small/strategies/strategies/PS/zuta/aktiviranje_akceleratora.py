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
		
	if State.must_stuck.val:
		r.absrot(-90)
		# r.setpos(y=-885)
		r.stuckpos(1, y=-885-5)
		r.forward(-100)
		
	r.goto(x,y+12-3-1,-1)
	r.absrot(0)
	rrucica(1)
	r.goto(x-120,y+12-3-1,-1)
	rrucica(0)
	State.goldenium_activated.val =1
	#####
	# Nakon sto gurne pak 
	#Poeni za guranje plavog u akcelerator i otklj goldeniuma
	addpts(10)
	addpts(10)

	
	r.forward(120) # dodao macak
	r.turn(-6)
	r.forward(-50) # dodao macak
def leave():
	rrucica(0)
