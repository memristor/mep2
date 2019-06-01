import numpy as np
weight = 20

def run():
	_print("blalblalaskdasf")
	'''	
	r.goto(0, 0)
	r.goto(-162, 90)
	r.forward(80)

	r.speed(120)
	r.absrot(200)

	@_spawn
	def _():
		lfliper(2)
	rfliper(2)
	
	_print("blalblalaskdasf")
	r.goto(*coord('haos_zona'))	


	r.turn(40)
	r.turn(-20)
	r.forward(-70)

	atoms = []
	@_do
	def _():
		nonlocal atoms
		print("tek sad ocitaj: ")
		atoms = cam_read()
		print("OCITAO")
		if len(atoms) > 1:
			for atom in atoms:
				print(atom)
			

	r.forward(60)
	
	@_spawn
	def _():
		lfliper(1)
	rfliper(1)

	@_spawn
	def _():
		lfliper(2)
	rfliper(2)
	
	r.forward(60)
	sleep(1)

	@_spawn
	def _():
		lfliper(1)
	rfliper(1)

	
	@_do
	def _():
		idx = np.argpartition([i[0] for i in atoms], int(len(atoms)/2))
		if atoms[idx[0]][1] < atoms[idx[1]][1]:
			desni = atoms[idx[0]][2]
			levi = atoms[idx[1]][2]
		else:
			desni = atoms[idx[1]][2]
			levi = atoms[idx[0]][2]

		postoji_crveni = False
		for i in range(2, len(idx)):
			if atoms[idx[i]][2] == 'red':
				postoji_crveni = True

		if postoji_crveni:
			r.goto(*coord('medja_cr_ze'))	
		else:
			x, y = coord('medja_pl_ze')
			r.goto((x, y))	
			r.goto((x+600, y), -1)	

		r.goto(*coord('periodni_priprema'), -1)	
		r.goto(*coord(levi))
		lfliper(2)
		r.goto(*coord('periodni_priprema'), -1)	
		lfliper(0)
		r.goto(*coord(desni))
		rfliper(2)
		r.goto(*coord('periodni_priprema'), -1)	
		rfliper(0)

	r.goto(*coord('periodni_priprema'), -1)	
	r.absrot(120)
	r.forward(100)

	@_do
	def _():
		nonlocal atoms
		sleep(1)
		atoms = cam_read()
		if len(atoms) > 0:
			@_spawn
			def _():
				lfliper(2)
			rfliper(2)
			r.forward(200)
			def _():
				lfliper(1)
			rfliper(1)

			x, y = coord(atoms[0][2])
			
			r.goto(x+200, y)
			r.absrot(200)
			@_spawn
			def _():
				lfliper(2)
			rfliper(2)
			
			r.forward(-200)
			def _():
				lfliper(0)
			rfliper(0)

		

	
	addpts(14) #Bodovi, ako je skupio celu haos zonu
	
	sleep(90)
	return
	_print("Kraj")
	'''
