#weight=1
#weight=10#dodatooooooo
def run():	
	sleep(0.3)
	r.speed(150)
	
	r.goto(500,50)
	r.goto(100,450)
	r.goto(0,500)
	r.goto(-150,500)
	r.goto(-1000,500)
	r.goto(-790,500,-1)
	r.goto(-790, 830)
	r.speed(40)
	r.conf_set('enable_stuck',0)
	r.goto(-600,830,-1)
	r.setpos(x=-610)
	r.goto(-705, 840)
	r.goto(-735, 870)
	r.goto(-840, 870)
	r.goto()
	
	
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
	
	r.speed(40)
	r.conf_set('enable_stuck', 0)	
	r.goto(-1150,1050)
	r.setpos(y=920)	
	sleep(0.5)
	klapna(2)
	r.speed(50)

	#####POZICIONIRANJE ZA SORTIRANJE####
	#dolazak na idealnu poziciju
	#r.goto(-1150,825,-1) # 1740,2474	
	r.forward(-120)	
	r.goto(-1000,825)
	r.goto(-955,825) #1740,2295
	sleep(0.5)
	cev2(1)
	for i in range(1):
		r.forward(20)
		sleep(0.05)
		r.forward(-20)
		sleep(0.05)
	for i in range(4):
		r.goto(-910,825)
		sleep(0.05)
		klapna(1)
		sleep(1)
		r.goto(-868,825)
		for i in range(1):
			r.forward(20)
			sleep(0.05)
			r.forward(-20)
			sleep(0.05)
		sleep(0.05)
		r.goto(-910,825,-1)
		sleep(0.05)
		klapna(2)
		r.goto(-955,825,-1)
		for i in range(1):
			r.forward(20)
			sleep(0.05)
			r.forward(-20)
			sleep(0.05)
			'''
