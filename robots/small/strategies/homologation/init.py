from core.Core import Core
from core.Util import Transform

def run():
	print('running homologation')
	r.conf_set('send_status_interval',100)
	
	r.setpos(58,-37)
	Core().transform = Transform(([58,-37],0), ([-1330,-920],90))
	r.softstop()
	r.speed(20)
	#  r.t(0)

	sleep(1000)
	return
	r.goto(705,-35)
	sleep(0.3)

	#  with disabler('collision'):
	# disable detection here
	for i in range(2):
		r.forward(25)
		sleep(0.01)
		r.forward(-25)
		sleep(0.01)
	sleep(0.5)
	# ....

	##########################
	######## PCELICA #########
	##########################

	r.goto(900,-35,-1)
	sleep(0.05)
	r.goto(1050,-430)
	r.goto(1150,-430)
	r.goto(1600,-95)
	sleep(0.05)
	r.turn(-180)
	pcelica(1)
	sleep(0.5)
	r.goto(1815,-95,-1)
	sleep(0.5)
	pcelica(0)
	sleep(1)
	r.forward(100)
	r.turn(180)
