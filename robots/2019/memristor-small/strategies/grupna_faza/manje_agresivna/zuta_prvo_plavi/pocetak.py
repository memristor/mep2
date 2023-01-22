weight= 10
State.a = _State(False)
# kupi prvi pak 
def run():
	
	# 90 je setpos
	r.speed(50)
	with disabled('collision'):
		r.curve_rel(187, -180+45+20)	
	r.speed(200) 
	
	r.goto(-762,-713,-1)
	
	### Bodovi za eksperiment
	addpts(40)
