weight= 4
State.a = _State(False)
# kupi prvi pak 
def run():
	
	# 90 je setpos
	r.speed(50)
	with disabled('collision'):
		r.curve_rel(187, -180)	
	r.speed(200) #bilo 180, picka
	
	### Bodovi za eksperiment
	addpts(40)
	
	
	#ide do cetvrtog
	r.goto(830,190,-1)
	@_spawn
	def _():
		nazgold(2)
	pump(1,1) # (br_pumpe,upaljena)

	r.goto(720,375,-1)
	r.speed(70) 
	r.goto(720,435,-1)
	sleep(0.3)
	

	r.goto(720,350,1)

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
			r.goto(300,370,-1)
			#r.goto(-735,300,1)
			_task_done()
			State.a.val = False
			return

	with disabled('collision'):
		r.speed(120)
		@_spawn
		def _():
			nazgold(1)
		sleep(0.3)
		r.goto(190-10,300)
		
		def f():
			_goto(offset=1, ref='main')
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f)
		r.goto(190-10,470,-1)
		r.speed(50)
		r.forward(-100)
		r.conf_set('enable_stuck', 0)

		p2 = nazadp.picked()		# Uhvatio ??????

		@_do						
		def _():
			if(p2.val):
				addpts(12) #crveni nosi 4 boda na vagi
				print("Dodao bodove ------------------------------")
			else:
				print("Nije uhvatio -------------------------")

		'''State.a.val = False

		pump(1,0)
		sleep(1)
		r.goto(190,210,1)'''

		State.a.val = False
		nazgold(2)
		sleep(0.5)
		pump(1,0)
		#sleep(5) zakomentarisano u testiranju
		nazgold(0)
		r.goto(190,210,1)
		
		






