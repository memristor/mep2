weight = 9


def run():
	
	
	x,y=coord('nase_case')

	sleep(0.5)
#casa1
	#pozicioniranje
	rfliper(2)
	if not pathfind(650,-700):
		return False
	sleep(3)
	#hvatanje
	@_spawn
	def _():	
		rfliper(1)
	rlift(0)
#pump(2, 1)
	#provera zahvata
#	p2 = sp_right.picked()
#	@_do
#	def _():
#		if (p2.val):
#			print("Uhvatio ------------------------------")
#		else:
#			print("Nije uhvatio -------------------------")
#			return False
	#podizanje
	rlift(1)
	sleep(0.1)
	r.absrot(180)
#casa2
	#pozicioniranje
	@_spawn
	def _():
		lfliper(2)
	r.curve_rel(-400,90)
	r.forward(170)
	lfliper(1)
	@_spawn
	def _():	
		rfliper(2)
	r.curve_rel(1050,48)
	rfliper(1)
	r.absrot(180)
	r.forward(150)
	r.speed(100)
	r.curve_rel(-900,90)
	r.absrot(90)
	r.forward(150)



