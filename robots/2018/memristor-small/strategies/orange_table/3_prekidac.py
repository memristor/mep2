weight=2
#  weight=20
def run():
	###############
	## PREKIDa
	###############

	r.speed(130)
	r.goto(-150, -114, -1) # r.goto(800,1060,-1)#######ZA PRVISTO10
	#sleep(5)
	r.goto(-450, -815, -1) # r.goto(100,1060, -1)
	r.speed(40)
	r.conf_set('enable_stuck', 1)
	def on_stuck():
		_next_cmd()
	_on('stuck', on_stuck)
	r.goto(-450, -964, -1) # r.goto(-50,1060, -1)
	
	#  r.setpos(300,-920, 90)
	r.setpos(y=-920)
	r.conf_set('enable_stuck', 0)
	
	r.speed(80)
	r.goto(-450, -815) # dodao 1 r.goto(100,1060)
	sleep(0.05)
	prekidac(1)
	sleep(0.1)
	r.goto(-450, -891, -1) #  r.goto(24, 1060, -1)
	sleep(0.5)
	r.goto(-450, -815) # r.goto(100, 1060)
	
	prekidac(0)
	#dodano nula
	#r.goto(0,0)
	#sleep(15)

	addpts(25)
	#r.goto(0,200) #sad dodali	

def leave():
	prekidac(0)
