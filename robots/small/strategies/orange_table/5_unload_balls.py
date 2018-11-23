weight=0
def run():
	#############################
	##  ISPUSTANJE PROTIVNICKIH
	#############################
	
	'''
	r.goto(610,820,-1)
	turbina(20)
	sleep(1)
	cev(0)
	sleep(3)
	turbina(0)
	
	addpts(20)
	'''
	#################################	
	
	
	r.goto(1200,830)
	r.goto(790,550)
	r.goto(100,550)
	r.goto(400,550,-1)
	with disabled('collision'):
		r.goto(400,660)
		r.speed(130)
		r.goto(400,730)
		r.setpos(y=670)
		klapna(2)
		cev2(0)
		for i in range(4):
			r.forward(-10)
			sleep(0.05)
			r.forward(10)
			sleep(0.05)
		
		r.conf_set('enable_stuck',0)
		r.forward(-35)
		r.speed(130)
		r.goto(400,730)	
		
		sleep(1)
		klapna(1)

	addpts(20)	
			
	r.goto(400,400,-1)
		
	return	
	
	r.goto(-136,485) #1400,1500
	#exit(0)
	return
	#r.conf_set('enable_stuck',0)
	r.goto(1650, 1500)
	sleep(0.5)
	klapna(2)
	cev2(0)
	sleep(3)
	#r.conf_set('enable_stuck',1)
	r.forward(-100)
	
	#############################
	## ISPALJIVANJE SORTIRANIH ##
	#############################
	r.goto(700,84, -1)
	r.goto(640,84, -1)
	#turbinaurn(190)
	sleep(2)
	turbina(80)
	sleep(3)
	cev(0)
	klapna(1)
	sleep(2)
	turbina(0)
	###############################
	#####ISPUSTANJE SORTIRANIH#####
	###############################
	klapna(2)

	##########################
