from core.Util import *
def run():
	r.conf_set('send_status_interval',10)
	State.color = (1280,-365)
	r.setpos(State.startpos[0],State.startpos[1],-90)
	r.speed(150)
