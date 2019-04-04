weight= 9
# kupi cetvrti pak 
def run():
	
	#r.goto(-830,190,-1)
	r.goto(-735,350,1)
	
	r.absrot(90)
	
		
	
	@_spawn
	def _():
		napgold(3)
	pump(2,1) # (br_pumpe,upaljena)
	r.speed(30)
	r.goto(-735,450,1) # kupi pomocu gold mehanizma
	sleep(0.5)
	napgold(0)

	r.speed(120)
	r.goto(-735,350,-1)
	
	'''@_do
	def _():
		if p1.val:
			State.pokupio = 1
	print('vrednost ', State.pokupio)'''
	

	
