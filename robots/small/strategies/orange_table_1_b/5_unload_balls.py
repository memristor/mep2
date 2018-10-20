import core.State as State
weight=0.2
def run():
	#############################
	##  ISPUSTANJE PROTIVNICKIH
	#############################

	if not state('loaded'):
		return False
		
	if not pathfind(136,610-50): #1400,1500
		return False
		
	r.conf_set('enable_stuck',1)
	def on_stuck():
		_next_cmd()
	_on('stuck', on_stuck)
	r.goto(136, 660)
	
	cev2(0)
	
	for i in range(3):
		klapna(1)
		sleep(0.5)
		klapna(2)
		sleep(0.5)
	r.goto(136, 610-50, -1)
	
	pathfind(-1500+300, -400)
	return
	#r.conf_set('enable_stuck',0)
	r.goto(1650, 1500)
	sleep(0.5)
	klapna(2)
	cev2(0)
	sleep(3)
	
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
