weight=20
def run():
	_print("nesto primio??")
	r.setpos(0, 0)
#r.forward(150)
#	r.forward(-100)
	r.speed(90)

	def skloni_pak():
		@_do
		def _():
			print("tek sad ocitaj: ")
			atoms = cam_read()
			if len(atoms) > 0:
				a = atoms[0]
				r.turn(-90)
				r.forward(int(-a[1]) + 120)
				r.turn(90)
				r.forward(int(a[0]) - 120)
				r.turn(90)
				r.forward(300)
				r.goto(0, 0, -1)
				r.absrot(0)
			sleep(90)

	r.conf_set('enable_stuck', 1)
	_on('motion:stuck', f)
	r.goto(45, 0)
