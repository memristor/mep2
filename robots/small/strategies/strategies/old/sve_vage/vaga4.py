weight= 13
# kupi prvi pak 
def run():
	if State.a.val == False:
		_task_suspend()
		return
	# nosi na vagu
	@_spawn
	def _():
		nazgold(1)
	r.goto(-200,350)

	def f():
		_goto(offset=1, ref='main')
	r.conf_set('enable_stuck', 1)
	_on('motion:stuck', f)
	r.goto(-200,470,-1)
	r.speed(50)
	r.forward(-100)
	r.conf_set('enable_stuck', 0)
	nazgold(2)
	sleep(0.5)
	pump(1,0)
	addpts(12)
	r.goto(-200,210,1)
	nazgold(0)

	State.a.val = False
	'''r.goto(-200,350)
	nazgold(1)
	r.goto(-200,470,-1)
	pump(1,0)
	r.goto(-200,350,1)'''

	
