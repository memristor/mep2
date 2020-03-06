
weight=10

def run():
	
#	@_spawn
#	def _():
#		lfliper(2)
	r.forward(57)
	r.curve_rel(-122, 52)

	sleep(5)
	#hvatanje
#	lfliper(1)
#	lok_visina(0)
	pump(1, 1)
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
#	lok_visina(1)

	#aktivacija tornja
	r.absrot(90)
	r.forward(-400)

	r.forward(100)

