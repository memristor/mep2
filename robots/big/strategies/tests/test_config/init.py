from core.Util import *

def run():
	r.conf_set('send_status_interval', 10)
	State.color = 'plava'

	State.startpos = (1360, -240)
	r.setpos(State.startpos[0], State.startpos[1], 90)

	r.speed(200)

	rok_visina(0)
	lok_visina(0)
	lfliper(0)
	rfliper(0)
