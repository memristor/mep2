weight= 4
# kupi prvi pak 
def run():
	
	# 90 je setpos
	r.speed(60)
	

	r.curve_rel(180, -180)
	
	
	r.speed(120)
	r.goto(830,260,-1)
	r.goto(520,360,-1)
	
	r.absrot(-90)
	@_spawn
	def _():
		nazgold(2)
	pump(1,1) # (br_pumpe,upaljena)
	r.speed(30)
	r.goto(635,442,-1)

	r.speed(120)
	r.goto(635,360,1)
	'''p1=nazadp.picked()
	@_do
	def _():
		if p1.val:
			State.pokupio = 1
	print('vrednost ', State.pokupio)'''
