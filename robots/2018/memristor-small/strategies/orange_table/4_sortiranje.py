weight=1

def run():	
	sleep(0.3)
	r.speed(150)

	y_sort = 820

	#r.goto(1200,1400)
	#return
	###################
	## SORTIRANJE
	#################
	cev(1)
	cev2(1)
	#pathfind(914,481) #1396,2278,-1
	sleep(0.05)
	if not pathfind(1140,785):
		return False
	#r.goto(1140,785,-1) #1700, 2493,-1
	sleep(0.05)
	r.speed(30)
	r.goto(1140,970,-1) # 1740,2474
	sleep(0.4)
	r.setpos(y=920)
	r.goto(1140,y_sort)
	r.speed(70)
	klapna(2)	
	r.goto(930,y_sort,-1)
	
	addpts(10)	

	for i in range(6):
		r.forward(25)
		sleep(0.05)
		r.forward(-25)
		sleep(0.05)

	r.goto(885,y_sort,-1)
	klapna(1)
	sleep(0.5)
	r.goto(840,y_sort,-1)
	sleep(0.2)

	for i in range(10):
		r.forward(20)
		sleep(0.05)
		r.forward(-20)
		sleep(0.05)
	
	sleep(0.5)
	
	return
		
	
	r.speed(50)

	#####POZICIONIRANJE ZA SORTIRANJE####
	#dolazak na idealnu poziciju
	r.goto(-900-40-15,818) #1740,2295
	sleep(0.5)
	r.conf_set('enable_stuck',0)
	cev2(1)
	for i in range(1):
		r.forward(20)
		sleep(0.05)
		r.forward(-20)
		sleep(0.05)
	for i in range(4):
		r.goto(-855-40-15,818)
		sleep(0.05)
		klapna(1)
		sleep(1)
		r.goto(-810-40-18,818)
		for i in range(1):
			r.forward(20)
			sleep(0.05)
			r.forward(-20)
			sleep(0.05)
		sleep(0.05)
		r.goto(-910,818,-1)
		sleep(0.05)
		klapna(2)
		r.goto(-955,818,-1)
		for i in range(1):
			r.forward(20)
			sleep(0.05)
			r.forward(-20)
			sleep(0.05)
