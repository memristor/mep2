weight= 10
State.a = _State(False)
# kupi prvi pak 
def run():
	
	# 90 je setpos
	r.speed(50)
	with disabled('collision'):
		r.curve_rel(-187, -180+45+20)	
	r.speed(200)
	r.goto(-762,-713,-1)
	### Bodovi za eksperiment	
	addpts(40)

	# testiranje samo haos zone
	# r.goto(0,0,-1)
	# r.goto(-169, 187,-1)
	# r.absrot(-90)
	# _task_done('haos_zona')


def leave():
	print('on leave1')
	_print('on leave2')
