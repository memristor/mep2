weight=0
def run():
	#############################
	##  ISPUSTANJE PROTIVNICKIH
	#############################

	#  r.goto(-1200,830,-1)
	if not pathfind(-1200,830):
		return False
	r.goto(-790,550)
	r.goto(-100,550)
	r.goto(-400,550,-1)
	with disabler('collision'):
		r.goto(-400,660)
		r.speed(130)
		r.goto(-400,730)
		r.setpos(y=670,o=90)
		cev2(0)
		for i in range(4):
			r.forward(-10)
			sleep(0.05)
			r.forward(10)
			sleep(0.05)

		r.conf_set('enable_stuck',0)

		r.forward(-35)
		r.speed(130)
		r.goto(-400,730)	
	
		sleep(1)
		klapna(1)
	
	addpts(20)
	return
	r.goto(-400,400,-1)

	return	

	with disabler('collision'):
		#r.goto(-400,730,-1)
		#r.setpos(y=670)
		#r.goto(-400,580)# 650 zeks
		r.goto(-1000,400,-1)
		r.goto(-750,650,-1)
		turbina(25)
	sleep(2)
	cev(0)
	sleep(8)
	turbina(0)
	r.forward(200)
	r.goto(0,0)
	return

	if not pathfind(-136+100,485): #1400,1500
		return False
	#exit(0)
	#  return
	r.conf_set('enable_stuck',1)
	r.goto(-36, 620)

	sleep(0.5)
	klapna(2)
	cev2(0)
	sleep(3)
	#r.conf_set('enable_stuck',1)
	r.forward(-100)
	cev2(1)
	
	return
	#############################
	## ISPALJIVANJE SORTIRANIH ##
	#############################
	r.goto(700,84, -1)
	r.goto(640,84, -1)
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
