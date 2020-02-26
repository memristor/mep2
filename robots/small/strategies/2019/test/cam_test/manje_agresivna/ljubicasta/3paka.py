from core.Util import *
_disabled=True
weight = 4
def run():

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
	
	if not _core.entities.get_entities_in_rect(rect_around_point([-1060,-240], [300,1000])):
		return False
	
	@_do
	def _():
		_core.entities.disable_entity('red_pack')

	
	#r.goto(*coord('3_paka_priprema'),-1)

	@_spawn
	def _():
		lfliper(2)
	rfliper(0)

	r.speed(100)
	#r.goto(*coord('3_paka_crveno'),1)
	r.goto(x+90,y-805)
	r.absrot(180)
	r.forward(180)
	addpts(13)
	r.forward(-180)
	lfliper(0)
	
	return

	
