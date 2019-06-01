weight= 98
# SA ZUTE STRANE!!
# krade cetvrti, tj. protivnicki plavi pak
def run():
	
	# 90 je setpos
	r.speed(160)
	
	r.goto(-718,280,1)
	r.absrot(-90)
	@_spawn
	def _():
		nazgold(3)
		pump(1,1) # (br_pumpe,upaljena)
	r.speed(30)
	sleep(0.1)
	r.goto(-715,460,-1) #zabadam se u pak
	sleep(0.3)

	r.speed(60)
	
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
			
			r.forward(50)
			
			_task_done()
			
	r.goto(-735+12+5,320,1) #izvlacenje
	r.speed(120)
	
	r.speed(160)
	r.goto(-200,0,-1)
	r.goto(169+30, 187,-1)
	#r.absrot(90)

	#r.curve_rel(-200, -180+10)
	
	with disabled('collision'):
		r.speed(120)	
		@_spawn
		def _():
			nazgold(1)
		r.goto(200-20-5,300+70,-1)

		def f():
			_goto(offset=1, ref='main')
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f)
		r.goto(200-20-5,470,-1)
		#r.forward(170)
		r.speed(50)
		r.absrot(270)
		r.forward(-100)
		r.conf_set('enable_stuck', 0)
	
	#Ostavljam protivnicki plavi pak na nasu vagu
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
	nazgold(2)
	sleep(0.3)		
	pump(1,0)
	sleep(0.5)
	nazgold(0)		
	r.goto(190,210,1)
