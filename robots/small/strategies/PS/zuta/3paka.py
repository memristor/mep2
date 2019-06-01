from core.Util import *
_disabled=True
#weight = 4
def run():

	return
	r.speed(150)	
	# r.forward(-330)
	
	# with disabled('collision'):
		
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)
	x,y=coord('3_paka_priprema')
	#r.goto(*coord('3_paka_priprema'),-1)
	# r.goto(x-40,y,-1)
	
	 
	if not pathfind(x-40,y):
		return False
	
	if _core.entities.get_entities_in_rect(rect_around_point([1060,-240], [300,800])):
		return False
	
	@_do
	def _():
		_core.entities.disable_entity('red_pack')

	
	#r.goto(*coord('3_paka_priprema'),-1)

	@_spawn
	def _():
		lfliper(0)
	rfliper(2)

	r.speed(100)
	#r.goto(*coord('3_paka_crveno'),1)
	r.goto(x-100,y-805)
	r.absrot(0)
	r.forward(180)
	addpts(13)
	r.forward(-180)
	rfliper(0)
	
	return


'''weight = 4
def run():

	r.speed(150)	
	r.forward(-330)
			
	with disabled('collision'):

		@_spawn
		def _():
			lfliper(0)
		rfliper(0)
		x,y=coord('3_paka_priprema')
		#r.goto(*coord('3_paka_priprema'),-1)
		r.goto(x+40,y+10,-1)
		@_spawn
		def _():
			lfliper(0)
		rfliper(2)
		
		r.speed(100)
		#r.goto(*coord('3_paka_crveno'),1)
		r.goto(x-40-30-5-10-5-10,y-855+30+20)
		r.absrot(0)
		r.forward(150+70-40)
		addpts(13)
		r.forward(-150-30)
		rfliper(0)
			
	return'''





	
