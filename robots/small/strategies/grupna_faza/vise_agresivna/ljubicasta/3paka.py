from core.Util import *
_disabled=True
weight = 4
def run():

	r.speed(160)	
	r.forward(-330)
			
	with disabled('collision'):

		@_spawn
		def _():
			lfliper(0)
		rfliper(0)

		x,y=coord('3_paka_priprema')
		r.goto(x-40,y+10,-1)
		r.absrot(270)

		@_spawn
		def _():
			lfliper(0)
		rfliper(2)
		
		r.speed(100)
		
		r.goto(x+70,y-805)
		r.absrot(0)
		r.forward(150+70-40)
		addpts(13)
		r.forward(-150-30-300)
		rfliper(0)
			
	return


	
