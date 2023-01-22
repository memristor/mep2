weight= 10
State.a = _State(False)
# kupi prvi pak 
def run():
	
	# 90 je setpos
	r.speed(50)
	with disabled('collision'):
		r.curve_rel(187, -180+45+20)	
	r.speed(140) #POVECATI KADA SE TESTIRA, OSTAVITI ILI SMANJITI AKO JE NESTABILNO
	
	### Bodovi za eksperiment
	addpts(40)

def leave():
	print('on leave1')
	_print('on leave2')
