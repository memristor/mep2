weight = 5
from core.Util import *
def run():
	_print('priprema za haos zonu !!')
	if not pathfind(169, 187):
		return False
	if not _core.entities.get_entities_in_rect(rect_around_point([800,0], [-1000,400])):
		return False
	#r.absrot(-90# ovo je odkomentarisano kod ljubicaste strane!)
	
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
	
	r.curve_rel(-520,44)
	r.curve_rel(440,27)
	@_spawn
	def _():
		lfliper(2)
	rfliper(2)
	r.absrot(0)	
	State.PS_mali.val=0
	r.forward(-300+20-300-250)
	State.PS_mali.val=0	
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)
	
	addpts(14) #Bodovi, ako je skupio celu haos zonu
	
	@_do
	def _():
		enable_task('3paka')
		_core.entities.disable_entity('haos_zona_zuta')
	# @_do
	# def finish():
		# _core.task_manager.clear_tasks()
	#State.PS_mali.val=0	
	return

	
def leave():
	r.forward(-200)
	
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)


'''weight = 5
def run():	
	
	@_spawn
	def _():
		lfliper(2)
	rfliper(2)	
	
	r.speed(120)
	r.goto(*coord('haos_zona'))
	
	r.forward(-35)
	
	@_spawn
	def _():
		lfliper(1)
	rfliper(1)
	
	r.forward(35)
	
	r.curve_rel(-500-20,48-6-2+1+3)
	r.curve_rel(330-20-20+150,34-3-2-2)	
	r.forward(-300+20)
	
	@_spawn
	def _():
		lfliper(0)
	rfliper(0)	
	
	addpts(14) #Bodovi, ako je skupio celu haos zonu
	return'''
	

