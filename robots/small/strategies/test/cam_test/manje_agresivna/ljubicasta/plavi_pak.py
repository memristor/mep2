weight = 6
State.a = _State(False)
def run():

	
	#ide do plavog
	r.speed(140)
	if not pathfind(-689,300):
		return False
	r.absrot(270)
	# r.goto(-720+5+5+21,350,-1)

	@_spawn
	def _():
		nazgold(3)
	pump(1,1) # (br_pumpe,upaljena)

	#r.goto(-720+5,375,-1)
	
	r.speed(70) 
	r.goto(-689,422,-1)
	sleep(0.3)	

	r.goto(-689,350,1) #Povlacim se nakon kupljenja
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
			#r.goto(-300,370,-1)	# Nije uhvatio, zavrsi
			#r.goto(-735,300,1)
			# r.goto(*coord('vaga'),1)
			# r.absrot(90)
			# r.forward(-350 + 50+25)
			_task_done()
			# State.a.val = False
			# return
	
	# with disabled('collision'):
	r.speed(120)	
	#@_spawn
	#def _():
		#nazgold(1)
	sleep(0.6)
	
	
	
	enable_task('3paka')
	'''r.absrot(90)
		
	with disabled('collision'):
		r.speed(120)	
		@_spawn			
		def _():
			napgold(1)
		sleep(0.6)
			#r.goto(-180,300)

		def f():
			_goto(offset=1, ref='main')
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f)
		r.goto(-200+20+5,470)	#Pred vagom KRITICNO
		#r.forward(170)
		r.speed(80)
		r.forward(100)
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
		napgold(2)
		sleep(0.5)		
		pump(2,0)
		sleep(0.3)
		napgold(0)		
		#r.goto(-190,210,1)
		r.forward(-300)'''










