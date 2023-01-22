weight= 4
# kupi prvi pak 
State.a = _State(False)
def run():
	
	# 90 je setpos
	r.speed(120)
	

	r.curve_rel(-180, -180)
	
	
	
	
	r.goto(-830,190,-1)
	r.goto(-1020,300,-1)
	
	r.absrot(-90)
	@_spawn
	def _():
		nazgold(2)
	pump(1,1) # (br_pumpe,upaljena)

	
	r.speed(30)
	r.goto(-1020,427,-1)

	r.speed(120)
	r.goto(-1020,250,1)
	
	p1 = nazadp.picked()		# Uhvatio ??????

	@_do						# Mora u _do da se proverava
	def _():
		if(p1.val):
			State.a.val = True
			print("Uhvatio ------------------------------")
		else:
			print("Nije uhvatio -------------------------")
			pump(1, 0)
			nazgold(0)	# Nije uhvatio, zavrsi
			r.goto(-735,300,1)
			_task_done()
			return
			
	'''
	@_do
	def _():
		if p1.val:
			State.pokupio = 1
	print('vrednost ', State.pokupio)'''
