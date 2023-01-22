weight= 4
# kupi prvi pak 
def run():
	
	# 90 je setpos
	r.speed(50)
	r.curve_rel(-180, -180)	
	r.speed(180)
	
	@_spawn
	def _():
		nazgold(2)
	pump(1,1) # (br_pumpe,upaljena)

	#ide do cetvrtog
	r.goto(-830,190,-1)

	r.goto(-735,375,-1)
	
	r.speed(180) 
	r.goto(-735,438,-1)
	sleep(0.3)
	

	r.goto(-735,350,1)
		
	@_spawn
	def _():
		nazgold(1)
	r.goto(-200,300)

	def f():
		_goto(offset=1, ref='main')
	r.conf_set('enable_stuck', 1)
	_on('motion:stuck', f)
	r.goto(-200,470,-1)
	r.speed(50)
	r.forward(-100)
	r.conf_set('enable_stuck', 0)
	pump(1,0)
	r.goto(-200,210,1)

