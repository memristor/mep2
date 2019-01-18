weight=2

def run():	
	sleep(0.3)
	r.speed(150)
	
	r.goto(-500,50)
	r.goto(150,500)
	r.goto(700,500)
	r.goto(1000,500)
	r.goto(790,500,-1)
	r.speed(30)
	r.goto(790, 770)
	r.conf_set('enable_stuck',0)
	r.goto(600,770,-1)
	r.setpos(x=610)
	r.goto(660,770)
	sleep(0.5)
	r.goto(710,780)
	r.goto(740,780)
	r.goto(920,775)
	r.goto(890,-155)
	
	
	sleep(5)
	'''
	#r.goto(1200,1400)
	#return
	###################
	## SORTIRANJE
	#################
	cev(1)
	r.goto(-914,481, -1) #1396,2278,-1
	sleep(0.05)
	r.goto(-1129,785, -1) #1700, 2493,-1
	sleep(0.05)
	r.goto(-1110,818) # 1740,2474
	sleep(0.5)
	klapna(2)
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
			'''
