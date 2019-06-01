weight= 11
# kupi prvi pak 
def run():
	# if State.pokupio == 0:
	#	pump(1,0)
	#	return
	# nosi na vagu
	if State.a.val == False:
		_task_suspend()
		return
	
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
	pump(1,0)
	addpts(4)	# Crveni u vagi dodaje 4 boda
	r.goto(-200,210,1)

	State.a.val = False
	'''r.goto(-200,350)
	nazgold(1)
	r.goto(-200,470,-1)
	pump(1,0)
	r.goto(-200,350,1)'''

	
