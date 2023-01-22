weight= 7
# kupi sesti pak 
def run():
	
	

	r.goto(-535,350,-1)
	
	r.absrot(-90)
	
	@_spawn
	def _():
		nazgold(2)
		pump(1,1) # (br_pumpe,upaljena)
	r.speed(30)
	sleep(0.5)
	r.goto(-535,450,-1)

	r.speed(120)
	r.goto(-535,350,1)


	'''
	@_do
	def _():
		if p1.val:
			State.pokupio = 1
	print('vrednost ', State.pokupio)
	'''


	

	
