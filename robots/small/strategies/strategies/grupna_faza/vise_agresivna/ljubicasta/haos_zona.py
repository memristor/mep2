weight = 5
from core.Util import *
def run():
	_print('priprema za haos zonu !!')
	if not pathfind(-169, 187):
		return False
	if not _core.entities.get_entities_in_rect(rect_around_point([-800,0], [1000,400])):
		return False
	r.absrot(-90)
	
	# sleep(10)
	r.speed(120)
	@_spawn
	def _():
		lfliper(2)
	rfliper(2)
	
	r.goto(*coord('haos_zona'))	
	
	
	r.forward(30)
	
	
	r.forward(230)
	r.goto(1156-30, -482-35-20)
	r.forward(-200)
	
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)
	
	addpts(14) #Bodovi, ako je skupio celu haos zonu
	
	@_do
	def _():
		enable_task('3paka')
		_core.entities.disable_entity('haos_zona')

	return

def leave():
	r.forward(-200)
	
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)
