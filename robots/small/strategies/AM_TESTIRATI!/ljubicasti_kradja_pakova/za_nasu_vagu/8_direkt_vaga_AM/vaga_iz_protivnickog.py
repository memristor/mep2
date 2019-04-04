weight = 9
def run():
	'''if State.pokupio == 0:
		pump(1,0)
		return'''
	r.goto(200,330,-1)
	r.absrot(90)
	r.curve_rel(200, -180)
	r.goto(-200,470,-1)
	pump(1,0)
	r.goto(-200,325,1)
