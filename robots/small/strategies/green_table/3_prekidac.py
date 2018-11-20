weight=2
#  weight=20
def run():
	###############
	## PREKID
	###############
	
	r.speed(130)
	if not pathfind(304, -815):
		return False
		
	r.speed(40)
	r.conf_set('enable_stuck', 1)
	def on_stuck():
		_next_cmd()
	_on('stuck', on_stuck)
	r.goto(304, -964, -1)
	
	r.setpos(y=-920)
	r.conf_set('enable_stuck', 0)
	
	r.speed(80)
	r.goto(304, -815)
	sleep(0.05)
	prekidac(1)
	sleep(0.1)
	r.goto(304, -891, -1)
	sleep(0.5)
	# r.goto(304, -815)
	r.goto(304, -815+100)
	
	prekidac(0)
	addpts(25)	


def leave():
	prekidac(0)
