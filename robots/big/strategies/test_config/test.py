weight = 1


def run():

	x, y = coord('srednje_blize')
	r.goto(x, y)
	if not pathfind(0, 0):
		return False


	rok_visina(1)
	lok_visina(1)

	lfliper(1)
	rfliper(1)

	rok_visina(0)
	lok_visina(0)

	lfliper(0)
	rfliper(0)



	pump(1, 1)
	p1 = sp_left.picked()  # Uhvatio ??????

	@_do
	def _():
		if (p1.val):
			r.goto(*State.startpos)
			print("Uhvatio ------------------------------")
		else:
			print("Nije uhvatio -------------------------")
			r.goto(1000, 1000)
	pump(1, 0)

	pump(2, 1)
	p1 = sp_left.picked()  # Uhvatio ??????

	@_do
	def _():
		if (p1.val):
			r.goto(*State.startpos)
			print("Uhvatio ------------------------------")
		else:
			print("Nije uhvatio -------------------------")
			r.goto(1000, 1000)
	pump(2, 0)

