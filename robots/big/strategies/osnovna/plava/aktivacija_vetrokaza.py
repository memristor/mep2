# weight = 2


def run():

	if not pathfind(700, -360):
		return False
	# Dosao do vetrokaza
	r.goto(750, 350)	
	r.goto(1300, 800)

	
	rrucica(1)
	_print("Izvukao ruku")

	r.absrot(180)
	#sleep(10)
	r.forward(430)
	rrucica(0)

	addpts(15)


