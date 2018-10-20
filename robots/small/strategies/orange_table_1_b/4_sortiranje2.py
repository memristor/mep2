weight=1

def run():	
	sleep(0.3)
	r.speed(150)

	if not pathfind(914,481, -1): #1396,2278,-1
		return False
	#r.goto(1200,1400)
	#return
	###################
	## SORTIRANJE
	#################
	cev(1)
		
	sleep(0.05)
	r.goto(1129,785, -1)
	sleep(0.05)
	
	y = 810
	r.goto(1110, y, -1)
	sleep(0.5)
	klapna(1)
	r.speed(50)

	#####POZICIONIRANJE ZA SORTIRANJE####
	#dolazak na idealnu poziciju
	 
	r.goto(955, y, -1)
	sleep(0.5)
	r.conf_set('enable_stuck',0)
	cev2(1)
	d=28
	#  for i in range(1):
		#  r.forward(-d)
		#  sleep(0.05)
		#  r.forward(d)
		#  sleep(0.05)
		
	for i in range(4):
		
		# middle
		r.goto(910,y,-1)
		sleep(0.05)
		klapna(2)
		sleep(1)
		r.goto(868,y, -1)
		
		# cimni ka +x
		for i in range(1):
			r.forward(d)
			sleep(0.05)
			r.forward(-d)
			sleep(0.05)
		
		
		sleep(0.05)
		
		# middle
		r.goto(910,y)
		sleep(0.05)
		klapna(1)
		r.goto(955,y)
		
		# cimni ka -x
		for i in range(1):
			r.forward(-d)
			sleep(0.05)
			r.forward(d)
			sleep(0.05)
			
	_do(lambda: state('loaded', True))
