#weight=0
def run():
	#############################
	##  ISPUSTANJE PROTIVNICKIH
	#############################

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
