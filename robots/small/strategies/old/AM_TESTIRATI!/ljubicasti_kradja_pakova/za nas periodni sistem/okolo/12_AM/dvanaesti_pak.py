weight= 10
# kupi 12. pak 
def run():
	
	# 90 je setpos

	r.curve_rel(-200, -180)
	r.speed(120)
	
	r.goto(-830,330,-1)#1. pak
	r.goto(-220,330,-1)#pre precke
	r.absrot(90)
	r.curve_rel(-220, -180)

	r.goto(1020,330,-1)#12. pak po x osi
	
	r.absrot(-90)
	@_spawn
	def _():
		#nazgold(2)
		pump(1,1) # (br_pumpe,upaljena)
	r.speed(30)
	r.goto(1020,438,-1)

	r.speed(120)
	r.goto(1020,330,1)
	'''p1=nazadp.picked()
	@_do
	=def _():
		if p1.val:
			State.pokupio = 1
	print('vrednost ', State.pokupio)'''
