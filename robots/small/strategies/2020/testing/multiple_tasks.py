weight = 2
_instances = 2
points = [ (100, 200), (-100, 200) ]

def run():
	_print('this is task number: ', _i)

	if not pathfind(*points[_i]):
		return False

	if _i < 4:
		levo_izvuci(0)
		levo_visina(1)
	else:
		desno_izvuci(0)
		desno_visina(1)

	pump(_i, 1)
	senzori = [sp1, sp2, sp3, sp4, sp5, sp6]

	p1 = senzori[_i].picked()
	@_do
	def _():
		if (p1.val):
			r.goto(*State.startpos)
			print("Uhvatio {} ------------------------".format(str(_i+1)))
		else:
			print("Nije uhvatio {} --------------------".format(str(_i+1)))
			r.goto(1000, 1000)
			pump(_i, 0)


