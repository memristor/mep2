from core.schedulers.SimulationScheduler import SimulationScheduler
def run():
	print('strategy init')
	_core.task_manager.set_scheduler(SimulationScheduler())
	State.strat_init.val = 'initialized'
