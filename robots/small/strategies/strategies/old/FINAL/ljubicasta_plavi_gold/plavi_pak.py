weight= 4
State.a = _State(False)
# kupi prvi pak 
def run():
	
	# 90 je setpos
	r.speed(50)
	r.curve_rel(-190, -180)	
	r.speed(180)
	
	### Bodovi za eksperiment
	addpts(40)

	@_spawn
	def _():
		nazgold(2)
	pump(1,1) # (br_pumpe,upaljena)

	#ide do cetvrtog
	r.goto(-820,190,-1)

	r.goto(-735+20,375,-1)
	
	r.speed(180) 
	r.goto(-735+20,433,-1)
	sleep(0.3)	

	r.goto(-735+20,350,1) #Povlacim se nakon kupljenja

	p1 = nazadp.picked()		# Uhvatio ??????

	@_do						
	def _():
		if(p1.val):
			State.a.val = True
			print("Uhvatio ------------------------------")
		else:
			print("Nije uhvatio -------------------------")
			pump(1, 0)
			nazgold(0)	# Nije uhvatio, zavrsi
			#r.goto(-735,300,1)
			_task_done()
			State.a.val = False
			return
		
	@_spawn
	def _():
		nazgold(1)
	r.goto(-200+20,300)

	def f():
		_goto(offset=1, ref='main')
	r.conf_set('enable_stuck', 1)
	_on('motion:stuck', f)
	r.goto(-200,470,-1)
	r.speed(50)
	r.forward(-100)
	r.conf_set('enable_stuck', 0)
	
	#Ostavljam plavi pak na vagu
	sleep(0.3)
	p2 = nazadp.picked()		# Uhvatio ??????

	@_do						
	def _():
		if(p2.val):
			addpts(12) #crveni nosi 4 boda na vagi
			print("Dodao bodove ------------------------------")
		else:
			print("Nije uhvatio -------------------------")

	State.a.val = False

	pump(1,0)
	r.goto(-200,210,1)








