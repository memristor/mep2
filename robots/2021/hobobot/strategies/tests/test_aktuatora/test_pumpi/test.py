weight = 1


def run():

	_print("************** Testiranje pumpe 1, leve")
	pump(1, 1)
	p1 = sp_left.picked()  # Uhvatio ??????

	@_do
	def _():
		if (p1.val):
			print("Uhvatio ------------------------------")
		else:
			print("Nije uhvatio -------------------------")

	sleep(2)
	pump(1, 0)


	_print("************** Testiranje pumpe 2, desne")

	pump(2, 1)
	p1 = sp_right.picked()  # Uhvatio ??????

	@_do
	def _():
		if (p1.val):
			print("Uhvatio ------------------------------")
		else:
			print("Nije uhvatio -------------------------")

	pump(2, 0)

