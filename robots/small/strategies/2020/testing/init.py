from core.Util import *

def run():
	r.conf_set('send_status_interval', 10)
	State.color = 'zuta'

	State.startpos = (1360, -40)
	r.setpos(State.startpos[0], State.startpos[1], 90)

	r.speed(200)

	levo_izvuci(0)
	desno_izvuci(0)
	levo_visina(0)
	desno_visina(0)
