
weight=10

def run():
	
	@_spawn
	def _():
		lfliper(2)
	_sync()
	r.curve_rel(-122, 52)
	r.forward(57)
	r.forward(20)

	#hvatanje
	lfliper(1)
	llift(0)	
	pump(0, 1)
	sleep(1)
	#provera zahvata
#	p1 = sp_left.picked()
#	@_do
#	def _():
#		if (p1.val):
#			print("Uhvatio ------------------------------")
#		else:
#			print("Nije uhvatio -------------------------")
#			return False
	llift(1)
	sleep(1)
	lfliper(0)

	#aktivacija tornja
	r.absrot(90)
	r.forward(-400)

	r.forward(100)

