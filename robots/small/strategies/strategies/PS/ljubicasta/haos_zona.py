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
	with _while(lambda: State.PS_veliki.val == 1):
		pass
	State.PS_mali.val=1
	@_spawn
	def _():
		lfliper(2)
	rfliper(2)
	r.goto(*coord('haos_zona'))	
	r.forward(-30)
	
	@_spawn
	def _():
		lfliper(1)
	rfliper(1)
	
	r.forward(30)
	
	r.curve_rel(520,44)
	r.curve_rel(-440,27)
	addpts(14) #Bodovi, ako je skupio celu haos zonu
	@_spawn
	def _():
		lfliper(2)
	rfliper(2)
	r.forward(-100)
	r.absrot(180)
	State.PS_mali.val=0
	r.forward(-280-300-100)
	
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)
	
	
	@_do
	def _():
		enable_task('3paka')
		_core.entities.disable_entity('haos_zona')
	# @_do
	# def finish():
		# _core.task_manager.clear_tasks()
		
	return

def leave():
	r.forward(-200)
	State.PS_mali.val=0
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)
