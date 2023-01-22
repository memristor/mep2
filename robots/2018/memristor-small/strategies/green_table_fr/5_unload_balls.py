#weight=0
def run():
	#############################
	##  ISPUSTANJE PROTIVNICKIH
	#############################

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
