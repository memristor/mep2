weight= 4
# kupi sesti pak 
def run():
	# 90 je setpos
	r.speed(120)
	

	r.curve_rel(-200, -180)
	

	
	
	r.goto(-830,260,-1)
	r.goto(-535,365,-1)
	
	r.absrot(-90)
	
	

	@_spawn
	def _():
		nazgold(2)
		pump(1,1) # (br_pumpe,upaljena)
	r.speed(30)
	sleep(0.5)
	r.goto(-535,442,-1)

	r.speed(120)
	r.goto(-535,365,1)


	'''
	@_do
	def _():
		if p1.val:
			State.pokupio = 1
	print('vrednost ', State.pokupio)
	'''


	

	
