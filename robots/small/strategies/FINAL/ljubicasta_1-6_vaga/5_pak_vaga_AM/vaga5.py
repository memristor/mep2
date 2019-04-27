weight= 3
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
	
	p2 = nazadp.picked()		# Uhvatio ??????

	if(p2.val):
		addpts(4) #crveni nosi 4 boda na vagi
		print("Dodao bodove ------------------------------")
	else:
		print("Nije uhvatio -------------------------")

	State.a.val = False

	pump(1,0)	# Crveni u vagi dodaje 4 boda
	r.goto(-200,210,1)

	'''r.goto(-200,350)
	nazgold(1)
	r.goto(-200,470,-1)
	pump(1,0)
	r.goto(-200,350,1)'''

	_task_suspend()
	return
