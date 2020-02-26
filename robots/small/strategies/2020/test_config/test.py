# weight = 1


def run():

	r.goto(1340, 900)
	if not pathfind(600, 0):
		return False


	levo_izvuci(0)
	desno_izvuci(0)
	levo_visina(1)
	desno_visina(1)

	pump(1, 1)
	p1 = sp1.picked()  # Uhvatio ??????

	@_do
	def _():
		if (p1.val):
			r.goto(*State.startpos)
			print("Uhvatio ------------------------------")
		else:
			print("Nije uhvatio -------------------------")
			r.goto(1000, 1000)

