weight=0
def run():
	#############################
	##  ISPUSTANJE PROTIVNICKIH
	#############################

	print('loaded: ', State.loaded.val)
	if not State.loaded.val:
		return False
		
	# if not pathfind(-400,550):
		# return False
	r.goto(-400,550,-1)
	with disabled('collision'):
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

		r.conf_set('enable_stuck', 0)

		r.forward(-35)
		r.speed(130)
		r.goto(-400,730)	
	
		sleep(1)
		klapna(1)
	
	addpts(20)
	r.goto(0,0,0)
