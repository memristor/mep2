weight= 10
# SA LJUBICASTE STRANJE!!
# krade deveti pak (na putu do tamo prodje kroz njihovu haos zonu da sve pakove u njima izgura) i stavlja u nasu vagu
def run():
	
	# 90 je setpos

	#r.curve_rel(-180, -130)
	r.speed(180)
	
	'''r.goto(-830,330,-1)#1. pak
	r.goto(-220,330,-1)#pre precke
	r.absrot(90)
	r.curve_rel(-220, -180)'''
	
	r.goto(820-60,320-20,-1)
	
	r.goto(735-60,320,-1)#4. pak po x osi
	
	r.absrot(-90)
	@_spawn
	def _():
		nazgold(2)
		pump(1,1) # (br_pumpe,upaljena)
	r.speed(30)
	r.goto(735-60,438,-1)

	r.speed(120)
	r.goto(735-60,320,1)
	'''p1=nazadp.picked()
	@_do
	=def _():
		if p1.val:
			State.pokupio = 1
	print('vrednost ', State.pokupio)'''
