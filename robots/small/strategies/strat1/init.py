from core.Core import Core
from core.Util import Transform
name ='...a_task...'
description='basic task'

task_instances = [
	{
		'weight': 5,
		'time': 7
	}
]

def leave():
	pass



def run():

	r.conf_set('send_status_interval',100)
	r.setpos(58,-37)
	Core().transform = Transform(([58,-37],0), ([-1500,-1000],-90))
	r.speed(100)
	r.t(0)
	
	#  r.turn(360)
	#  r.turn(360)
