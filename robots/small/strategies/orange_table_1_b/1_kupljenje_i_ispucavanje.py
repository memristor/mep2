
weight=20
def run():
	#  r.send(b'R')
	#load_cfg(r)
	#
	_unlisten('collision')
	r.speed(120)###PROMJENIO SA 100  
	turbina(0)
	klapna(1)
	cev(0)
	turbina(85) ###########
	sleep(0.5)
	r.goto(-1316, -195) #  r.goto(720,48)

	for i in range(8):
		r.forward(25)
		sleep(0.01)
		r.forward(-25)###plavi vratio na -25 bilo -30
		sleep(0.01) 

	sleep(0.5)
	r.forward(-100) #promjenio sa -200
	turbina(0)
	#  r.goto(-934, 135) # r.goto(1050, 430)
	

	
	

	return
	r.conf_set('enable_stuck',0)
	cev2(1)
	return
	r.forward(-70)
	return
	r.goto(674,524)#1439,2038
	return
	

	
	exit(0)

