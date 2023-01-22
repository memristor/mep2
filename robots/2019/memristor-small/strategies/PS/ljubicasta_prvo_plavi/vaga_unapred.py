weight = 70


def leave_front():
	
	if not pathfind(-169-30, 187): #dodato -30 zbog precke u sredini da ne zakaci slucajno
		return False
	#nosi ga na vagu
	r.speed(200)
	
	p3 = napredp.picked()		

	@_do						# Mora u _do da se proverava
	def _():
		if(p3.val):
			addpts(20) #uzeo gold
			print("Uhvatio ------------------------------")
		else:
			print("Nije uhvatio -------------------------")
			pump(2, 0)
			nazgold(0)	# Nije uhvatio, zavrsi
			r.goto(-168,170-40)
			# _task_done()
			State.goldenium_picked.val = 0
			_task_suspend()
			return
	
	r.goto(-200+13+13+5+10-1,250-20,1)
	p4 = napredp.picked()		# Uhvatio ??????

	@_do						
	def _():
		if(p4.val):
			addpts(24) #crveni nosi 4 boda na vagi
			print("Dodao bodove ------------------------------")
		else:
			print("Nije uhvatio -------------------------") #otkomentarisano
			State.back.val = 0
				
	with disabled('collision'):
		def f():
			_goto(offset=1, ref='main')
		r.conf_set('enable_stuck', 1)
		_on('motion:stuck', f)
		r.goto(*coord('vaga'),1) # originalno -200+13
		r.speed(50)
		r.absrot(90)
		r.forward(100)
		r.conf_set('enable_stuck', 0)
		r.speed(50)
		napgold(1)
		sleep(0.3)
		pump(2,0)
		sleep(0.5)
	# Provera da li je isporucen goldenium da bi sabrao bodove
	with disabled('collision'):
		r.forward(-10)
	pump(2,0)
	sleep(0.5)
	napgold(0)   #treba 0!
	sleep(0.2)
	r.forward(-350 + 50+25) #dodato +50
	State.goldenium_picked.val = 0

def leave_back():
	
	if not pathfind(-169, 187):
		return False
	#r.goto(-180,300)	
	def f():
		_goto(offset=1, ref='main')
	r.conf_set('enable_stuck', 1)
	_on('motion:stuck', f)
	r.goto(-200+20+5+3+5,470,-1)	#Pred vagom KRITICNO
	#r.forward(170)
	r.absrot(270)
	r.speed(80)
	r.forward(-100)
	r.conf_set('enable_stuck', 0)

	#Ostavljam plavi pak na vagu
	sleep(0.3)
	p2 = nazadp.picked()		# Uhvatio ??????

	@_do					
	def _():
		if(p2.val):
			addpts(12) #plavi nosi 12 boda na vagi
			print("Dodao bodove ------------------------------")
		else:
			print("Nije uhvatio -------------------------")
			State.back.val = 0
			_task_suspend()


	# State.a.val = False
	nazgold(2)
	sleep(0.5)		
	pump(1,0)
	sleep(0.5)
	nazgold(0)
	State.back.val = 0		
	r.forward(300)

def run():

	if State.goldenium_picked.val:
		leave_front()
	elif State.back.val:
		leave_back()
	else:
		return False
	_task_suspend()
	


