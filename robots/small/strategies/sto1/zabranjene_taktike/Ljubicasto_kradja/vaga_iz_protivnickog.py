weight = 9
def run():
	'''if State.pokupio == 0:
		pump(1,0)
		return'''
	r.goto(200,330,-1)
	r.absrot(90)

	r.curve_rel(200, -180)
	
	with disabled('collision'):
		r.speed(120)	
		@_spawn
		def _():
			nazgold(1)
		r.goto(-200+20+5,300)

		def f():
			_goto(offset=1, ref='main')
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f)
		r.goto(-200+20+5,470,-1)
		#r.forward(170)
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

	'''State.a.val = False

	pump(1,0)
	r.goto(-190,210,1)'''

	State.a.val = False
	nazgold(2)
	sleep(0.5)		
	pump(1,0)
	#leep(5)zakomentarisano u testiranju
	nazgold(0)		
	r.goto(-190,210,1)
	
	'''def f():
		_goto(offset=1, ref='main')
	r.conf_set('enable_stuck', 1)
	_on('motion:stuck', f)
	r.goto(-200+20,470,-1)
	r.speed(50)
	r.forward(-100)
	r.conf_set('enable_stuck', 0)
	nazgold(2)
	sleep(0.5)
	pump(1,0)
	addpts(12)
	sleep(0.5)
	
	r.goto(-200,210,1)

	r.goto(-200,470,-1)
	pump(1,0)
	r.goto(-200,325,1)'''
