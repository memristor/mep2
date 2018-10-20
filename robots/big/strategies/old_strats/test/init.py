name ='...a_task...'
description='basic task'


def run():
	#  lift(1)
	rotate(0)
	#  rotate(0)
	sleep(0.1)
	rotate(3)
	sleep(0.1)
	rotate(2)
	return
	def par():
		#  sleep(3)
		#  pump(0,1)
		rotate(0)
		rotate(3)
		_label('sync1')
	
	c=_spawn(par)
	
	#  r.goto(1000,0)
	#  return
	
	
	lift(1)
	
	#sleep(2.5)
	
	lift(0)
	_sync(c,'sync1')
	#  c=_spawn(par)
	#  r.goto(0,0)
	rotate(2)
	#  pump(0,0)
	
