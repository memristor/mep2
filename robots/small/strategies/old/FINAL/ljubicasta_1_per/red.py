weight = 3
def run():
	if State.a.val == False:
		pump(1,0)
		_task_suspend()
		return
	r.goto(-800,250)
	r.goto(-800,-550,1)
	r.goto(-1100,-550,-1) # da pak ispred polja da ne bi ovaj sa pumpe lupio u njega 
	#r.goto(-1270,-550)
	#r.goto(-1170,-550) # kada mali pogura pakove dalje ka zidu
	r.goto(-1000,-550,1)
	r.turn(15)
	
	p2 = nazadp.picked()		# Uhvatio ??????

	if(p2.val):
		addpts(6) #crveni nosi 4 boda na vagi
		print("Dodao bodove ------------------------------")
	else:
		print("Nije uhvatio -------------------------")

	State.a.val = False
	
	pump(1,0)
	
