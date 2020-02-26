weight = 3
_instances = 9


koordinate = [
	'vetrokazi',
	'nase_case',
	'srednje_blize',
	'srednje_dalje',
	'mala_luka',
	'velika_luka',
	'marina_sever',
	'marina_jug',
	'aktivacija_tornja'
]

def run():
	_print('This task checks coordinate for: ', koordinate[_i])

	if not pathfind(*coord(koordinate[_i])):
		return False
	_print("Stigao do: " + koordinate[_i])

	p1 = sp1.picked()

	@_do
	def _():
		if (p1.val):
			print("Uhvatio {} ------------------------".format(str(_i + 1)))
		else:
			print("Nije uhvatio {} --------------------".format(str(_i + 1)))
			r.goto(0, 0)
			pump(_i, 0)



