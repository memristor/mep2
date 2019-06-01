weight = 3
def run():

	# Pak za guranje 1300cm od ivice, 774
	# Pak za guranje: (200,1000)
	# Goldium: (726,1000)
	
      
	
	r.speed(180)
	#r.goto(160,-860,1)
	r.goto(450, -600)
	r.absrot(-90)

	r.speed(60)	
		
	def f():
		_goto(offset=1, ref='main')
	r.conf_set('enable_stuck', 1)
	_on('motion:stuck', f)
	r.goto(450,-800)
	r.absrot(-90)
	r.forward(150)
	r.setpos(y=-885)
	r.conf_set('enable_stuck', 0)

	r.speed(180)

	r.forward(-100)
	r.absrot(0)
	r.goto(160,-835,-1)
	r.absrot(0)
	rrucica(1)
	r.forward(120)
	rrucica(0)
	#####
	# Nakon sto gurne pak 
	#Poeni za guranje plavog u akcelerator i otklj goldeniuma
	addpts(10)
	addpts(10)

	r.forward(-50)
	r.turn(10)
	
	r.goto(720,-750)
	#r.forward(500) #Umesto ovoga treba da napisemo koordinate da bi uvek dosao na isto 430 -755
	r.absrot(-90)

	napgold(2)
	sleep(0.1)
	pump(2,1)
	# Implementirati stak umesto ovoga
	r.forward(85)
	sleep(0.3)
	
	r.forward(-100)
	sleep(0.3)

	#Kupi goldenium

	p3 = napredp.picked()		

	@_do						# Mora u _do da se proverava
	def _():
		if(p3.val):
			State.a.val = True
			addpts(20) #Uzimanje goldeniuma
			print("Uhvatio ------------------------------")
		else:
			print("Nije uhvatio -------------------------")
			pump(2, 0)
			nazgold(0)	# Nije uhvatio, zavrsi
			#r.goto(-735,300,1)
			_task_done()
			return
	
	#nosi ga na vagu
	napgold(0)
	r.goto(-200,250-20,1)
	def f():
		_goto(offset=1, ref='main')
	r.conf_set('enable_stuck', 1)
	_on('motion:stuck', f)
	r.goto(-200+15,470,1)
	r.speed(50)
	r.absrot(90)
	r.forward(100)
	
	r.conf_set('enable_stuck', 0)
	r.speed(180)
	napgold(1)


	# Provera da li je isporucen goldenium da bi sabrao bodove
	p4 = napredp.picked()		# Uhvatio ??????

	@_do						
	def _():
		if(p4.val):
			addpts(24) #crveni nosi 4 boda na vagi
			print("Dodao bodove ------------------------------")
		else:
			print("Nije uhvatio -------------------------")

	State.a.val = False
	
	pump(2,0)
	sleep(1)
	r.forward(-100)
	r.forward(-1000)
	r.goto(*State.startpos)




