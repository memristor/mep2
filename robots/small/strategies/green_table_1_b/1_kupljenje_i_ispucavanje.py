import core.State
weight=20
def run():
	#  r.send(b'R')
	#load_cfg(r)
	#
	#r.softstop()
	#sleep(200)
	#  sleep(300)
	_unlisten('collision')
	r.speed(130)###PROMJENIO SA 100 
	turbina(0)
	klapna(1)
	cev(0)
	turbina(90) ###########
	sleep(0.5)
	
	addpts(10)
	core.State.cnt = 0
	r.goto(1316, -195) #  r.goto(720,48)
	#  if not pathfind(1316, -195): #  r.goto(720,48)
		#  print('should quit')
		#  return False
	
	
	for i in range(8):
		r.forward(30)
		sleep(0.01)
		r.forward(-30)###bio -25
		sleep(0.01) 

	
	sleep(0.5)
	
	#  r.goto(934, 135) # r.goto(1050, 430)
	
	
def leave():
	r.forward(-100) #promjenio sa -200
	turbina(0)
