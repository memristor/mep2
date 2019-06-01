aktivirao = _State(0)
weight = 8
def run():

	# Pak za guranje 1300cm od ivice, 774
	# Pak za guranje: (200,1000)
	# Goldium: (726,1000)
	if not State.goldenium_activated.val:
		return False
	
	x,y=coord('goldenium')
	#r.goto(*coord('goldenium'))
	if not pathfind(x+16,y+8):
		return False
	r.absrot(-90)	#namesti se pred goldiumom
	napgold(2)
	sleep(0.3)
	pump(2,1)
	r.speed(60)
	r.forward(96)
	sleep(0.3)	#nataknut na gold i uzima ga
	r.speed(140)
	r.forward(-86)
	sleep(0.2)
	napgold(0)  #treba 0
	
	State.goldenium_picked.val = 1




