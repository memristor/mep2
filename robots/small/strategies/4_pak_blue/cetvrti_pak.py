weight= 10
# kupi prvi pak 
def run():
	
	# 90 je setpos

	r.curve_rel(-200, -180)
	r.speed(120)
	
	r.goto(-830,190,-1)
	r.goto(-720,300,-1)
	
	r.absrot(-90)
	@_spawn
	def _():
		#nazgold(2)
		pump(1,1) # (br_pumpe,upaljena)
	r.speed(30)
	r.goto(-720,450,-1)

	r.speed(120)
	r.goto(-720,300,1)
	p1=nazadp.picked()
	@_do
	def _():
		if p1.val:
			State.pokupio = 1
	print('vrednost ', State.pokupio)