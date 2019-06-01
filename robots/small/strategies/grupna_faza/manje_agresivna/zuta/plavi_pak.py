weight = 6
State.a = _State(False)
def run():

	
	#ide do plavog
	r.speed(140)
	if not pathfind(689,300):
		return False
	#r.absrot(270)
	# r.goto(-720+5+5+21,350,-1)

	@_spawn
	def _():
		nazgold(2)
	pump(1,1) # (br_pumpe,upaljena)

	#r.goto(-720+5,375,-1)
	
	r.speed(70) 
	r.goto(689,422,-1)
	sleep(0.3)	

	r.goto(689,350,1) #Povlacim se nakon kupljenja
	nazgold(0) 
	
	

	p1 = nazadp.picked()		# Uhvatio ??????

	@_do						
	def _():
		if(p1.val):
			State.a.val = True
			State.back.val = True
			print("Uhvatio ------------------------------")
		else:
			print("Nije uhvatio -------------------------")
			pump(1, 0)
			nazgold(0)
			r.forward(100)
			_task_done()
	
	# with disabled('collision'):
	r.speed(120)	
	@_spawn
	def _():
		nazgold(1)
	sleep(0.6)











