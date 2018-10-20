weight=1
#weight=100
def run():	
	sleep(0.3)
	r.speed(150)

	
	#r.goto(1200,1400)
	#return
	###################
	## SORTIRANJE
	#################
	cev(1)
	#  r.goto(-914,481, -1) #1396,2278,-1
	#  pathfind(-914, 481, -1)
	
	#  sleep(0.05)
	if not pathfind(-1129,785): #1700, 2493,-1
		return False
	#  sleep(0.05)
	y=838
	r.goto(-1110,y) # 1740,2474
	#  sleep(0.5)
	#  r.setpos(-1500+80+60, 1000-60-130,0)
	#  r.softstop()
	#  sleep(200)
	klapna(2)

	#####POZICIONIRANJE ZA SORTIRANJE####
	#dolazak na idealnu poziciju
	
	r.goto(-900-40-15,y) #1740,2295
	r.speed(50)
	sleep(0.5)
	r.conf_set('enable_stuck',0)
	cev2(1)
	for i in range(1):
		r.forward(20)
		sleep(0.05)
		r.forward(-20)
		sleep(0.05)
	for i in range(4):
		r.goto(-855-40-15,y)
		sleep(0.05)
		klapna(1)
		sleep(1)
		r.goto(-810-40-18,y)
		for i in range(1):
			r.forward(20)
			sleep(0.05)
			r.forward(-20)
			sleep(0.05)
			
		sleep(0.05)
		r.goto(-910,y,-1)
		sleep(0.05)
		klapna(2)
		r.goto(-955,y,-1)
		
		for i in range(1):
			r.forward(20)
			sleep(0.05)
			r.forward(-20)
			sleep(0.05)
	r.goto(-1110,818,-1)
	r.forward(-100)

