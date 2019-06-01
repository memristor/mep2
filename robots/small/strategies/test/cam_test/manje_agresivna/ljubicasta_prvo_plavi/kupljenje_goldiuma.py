aktivirao = _State(0)
weight = 6
def run():

	# Pak za guranje 1300cm od ivice, 774
	# Pak za guranje: (200,1000)
	# Goldium: (726,1000)
	if not State.goldenium_activated.val:
		return False
	
	x,y=coord('goldenium')
	#r.goto(*coord('goldenium'))
#r.goto(x+5+10+1,y-50+15+10+5+10-1-1,-1)
	if not pathfind(x+5+10+1,y-50+15+10+5+10-1-1+20):
		return False
	r.absrot(-90)

	napgold(2)
	sleep(0.3)
	pump(2,1)
	r.speed(60)
	r.forward(90-2-10-2+20)
	sleep(0.3)
	r.speed(140)
	r.forward(-100+2+10+2)
	sleep(0.2)
	napgold(0)  #treba 0
	
	State.goldenium_picked.val = 1




