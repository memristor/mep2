weight = 3
def run():

	# Pak za guranje 1300cm od ivice, 774
	# Pak za guranje: (200,1000)
	# Goldium: (726,1000)
	r.speed(80)
	r.goto(-1195,-775,-1)
	r.absrot(-180)
	r.goto(-140,-775,-1)
	r.goto(-140,190,-1)
	
	#r.absrot()
	@_spawn
	def _():
		lfliper(2)
	rfliper(2)	
	
	r.goto(-512,35)
	
	#r.goto(-716,-90)
	r.goto(-1156, -482)
	
	r.goto(-400,0,-1)
	State.PS_mali.val=1
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)	
	return
	
