from core.Util import *
State.goldenium_activated = _State(0)
State.goldenium_picked = _State(0)
# State.back = _State(0, name='back', shared=True) #Za serovane promenljive izmedju robota
State.back = _State(0)


def run():
	r.conf_set('send_status_interval', 10)
	State.color = 'ljubicasta'
	State.startpos = (-1195, -610)
	r.setpos(-1500+175+138,-610,90) # red
	_core.entities.add_entity('pathfind', 'red_pack', polygon_from_rect(rect_around_point([-1000,30], 50)))
	napgold(0)
	nazgold(0)
	rrucica(0)
	lrucica(0)
	rfliper(0)
	lfliper(0)
	r.speed(50)
	experiment('1')
	
	
