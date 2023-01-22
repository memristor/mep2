from core.Util import *

def run():
	r.conf_set('send_status_interval', 10)
	State.color = 'plava'

	State.startpos = (1500-255, 1000-765)#1280, -365
	r.setpos(State.startpos[0], State.startpos[1], 90)#90 = -90

	r.speed(200)

	#rlift(1)
	#llift(1)
	#lfliper(0)
	#rfliper(0)
